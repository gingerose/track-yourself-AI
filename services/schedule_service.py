from repositories.plan_repository import PlanRepository
from utils.data_preprocessing import preprocess_data
from utils.lstm_model import build_lstm_model, predict_schedule
from datetime import timedelta, datetime


class ScheduleService:
    def __init__(self, db):
        self.plan_repo = PlanRepository(db)

    def get_week_start(self, date_str):

        date = datetime.strptime(date_str, "%d.%m.%Y").date()
        return date - timedelta(days=date.weekday())

    def filter_by_deadline(self, plans, week_start):

        week_start_date = week_start
        return [plan for plan in plans if plan.deadline >= week_start_date]

    def generate_schedule(self, user_id, date):
        week_start = self.get_week_start(date)
        plans = self.plan_repo.get_plans_by_user_before_date(user_id, week_start)

        if not plans:
            return None, "No plans found for the user."

        plans = self.filter_by_deadline(plans, week_start)

        if not plans:
            return None, "No tasks for this week based on deadlines."

        plans_data = preprocess_data(plans)
        productivity_schedule = predict_schedule(plans_data)

        result = []
        for i, plan in enumerate(plans):
            schedule_item = {
                'plan_id': plan.plan_id,
                'name': plan.name,
                'description': plan.description,
                'status': plan.status,
                'creation_date': plan.creation_date.strftime('%Y-%m-%d'),
                'day_of_week': (week_start + timedelta(days=i % 7)).strftime('%A'),
                'priority': plan.priority,
                'modify_date': plan.modify_date.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': plan.duration,
                'deadline': plan.deadline.strftime('%Y-%m-%d'),
                'time_of_day': productivity_schedule[i],
            }
            result.append(schedule_item)

        result = sorted(result, key=lambda x: (x['time_of_day'] == 'morning', x['priority']), reverse=True)

        return result, None
