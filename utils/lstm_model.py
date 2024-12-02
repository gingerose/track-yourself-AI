import random

import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential

from loger import Logger
from models.plan import Plan


def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dense(7, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def augment_data(plans):
    priority_mapping = {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}
    augmented_plans = []
    for plan in plans:
        numeric_priority = priority_mapping[plan.priority]
        augmented_priority = max(0, min(3, numeric_priority + random.choice([-1, 0, 1])))
        augmented_priority_str = [k for k, v in priority_mapping.items() if v == augmented_priority][0]
        augmented_plan = Plan(
            plan_id=plan.plan_id,
            user_id=plan.user_id,
            name=plan.name,
            description=plan.description,
            status=random.choice(['IN_PROGRESS', 'DELAY', 'DONE']),
            creation_date=plan.creation_date,
            day_of_week=plan.day_of_week,
            priority=augmented_priority_str,
            modify_date=plan.modify_date,
            duration=plan.duration + random.randint(-1, 2),
            deadline=plan.deadline
        )
        augmented_plans.append(augmented_plan)
    return augmented_plans


def preprocess_lstm_data(plans, reference_date):
    data = pd.DataFrame([{
        'status': plan.status,
        'priority': plan.priority,
        'duration': plan.duration,
        'deadline_days_left': (plan.deadline - reference_date).days,
        'modify_hour': plan.modify_date.hour if plan.modify_date else 0
    } for plan in plans])
    data['status'] = data['status'].map({'IN_PROGRESS': 1, 'DELAY': 1, 'NOT_ACTUAL': 0, 'EMPTY': 0, 'DONE': 0})
    data['priority'] = data['priority'].map({'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0})
    data['duration'] /= 12
    data['modify_hour'] /= 24
    data['deadline_days_left'] /= 7
    return data.values.reshape((data.shape[0], 1, data.shape[1]))


def suggest_best_time(plans):
    time_of_day_count = {'morning': 0, 'afternoon': 0, 'evening': 0}
    for plan in plans:
        if plan.modify_date:
            hour = plan.modify_date.hour
            if 8 <= hour < 12:
                time_of_day_count['morning'] += 1
            elif 12 <= hour < 17:
                time_of_day_count['afternoon'] += 1
            elif 17 <= hour < 22:
                time_of_day_count['evening'] += 1
    best_time_of_day = max(time_of_day_count, key=time_of_day_count.get)

    return best_time_of_day


def suggest_least_productive_time(best_time):
    if best_time == 'morning':
        return 'evening'
    elif best_time == 'afternoon':
        return 'morning'
    elif best_time == 'evening':
        return 'afternoon'


from collections import defaultdict
import numpy as np


def distribute_schedule(plans, day_predictions, max_hours_per_day=12):
    week_schedule = defaultdict(list)
    day_load = np.zeros(7, dtype=int)
    best_time = suggest_best_time(plans)
    least_productive_time = suggest_least_productive_time(best_time)

    for plan, day in zip(plans, day_predictions):
        duration = plan.duration
        if plan.priority == 'CRITICAL':
            plan_time_suggestion = best_time
        elif plan.priority == 'MEDIUM':
            plan_time_suggestion = 'afternoon' if best_time == 'morning' else 'morning'
        else:
            plan_time_suggestion = least_productive_time

        for offset in range(7):
            current_day = (day + offset) % 7

            if day_load[current_day] + duration <= max_hours_per_day or offset == 6:
                week_schedule[current_day + 1].append({
                    'plan_id': plan.plan_id,
                    'name': plan.name,
                    'description': plan.description,
                    'status': plan.status,
                    'priority': plan.priority,
                    'duration': duration,
                    'deadline': plan.deadline.strftime('%Y-%m-%d'),
                    'suggested_time': plan_time_suggestion
                })
                day_load[current_day] += duration
                break

    empty_days = [i + 1 for i, load in enumerate(day_load) if load == 0]
    if empty_days:
        redistribute_tasks_to_empty_days(week_schedule, empty_days, max_hours_per_day)

    return dict(week_schedule)


def redistribute_tasks_to_empty_days(schedule, empty_days, max_hours_per_day):
    for day in empty_days:
        for existing_day in sorted(schedule.keys()):
            tasks = schedule[existing_day]
            for task in tasks:
                if task['priority'] == 'LOW' and task['duration'] <= max_hours_per_day:
                    schedule[day].append(task)
                    tasks.remove(task)
                    break
            if schedule[day]:
                break


def filter_plans(plans, reference_date):
    start_of_week = reference_date - pd.Timedelta(days=reference_date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=6)

    filtered_plans = [plan for plan in plans if
                      plan.status not in {'NOT_ACTUAL', 'DONE'} and start_of_week <= plan.deadline <= end_of_week]

    filtered_plans.sort(key=lambda x: x.deadline)

    return filtered_plans


def predict_schedule(plans_data, reference_date, days_in_week=7, max_hours_per_day=12):
    filtered_plans = filter_plans(plans_data, reference_date)
    augmented_plans = augment_data(filtered_plans)
    X = preprocess_lstm_data(augmented_plans, reference_date)
    model = build_lstm_model((X.shape[1], X.shape[2]))

    early_stopping = EarlyStopping(monitor='val_loss', patience=5)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.001)

    y = np.eye(days_in_week)[np.random.choice(days_in_week, len(X))]
    model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2,
              callbacks=[early_stopping, reduce_lr, Logger], verbose=0)

    y_pred = model.predict(X)
    day_blocks = np.argmax(y_pred, axis=1)

    week_schedule = distribute_schedule(filtered_plans, day_blocks, max_hours_per_day)
    return week_schedule
