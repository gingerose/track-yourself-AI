import pandas as pd

def preprocess_data(plans):

    data = pd.DataFrame([{
        'day_of_week': plan.day_of_week,
        'priority': plan.priority,
        'status': plan.status,
        'creation_date': plan.creation_date,
        'modify_date': plan.modify_date,
        'duration': plan.duration,
        'deadline': plan.deadline
    } for plan in plans])

    data['priority'] = data['priority'].map({
        'CRITICAL': 4,
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1
    })

    data['status'] = data['status'].map({
        'EMPTY': 3,
        'IN_PROGRESS': 4,
        'NOT_ACTUAL': 1,
        'DONE': 2
    })


    data['deadline'] = pd.to_datetime(data['deadline'], errors='coerce')
    data['days_to_deadline'] = (data['deadline'] - pd.Timestamp.now()).dt.days.fillna(0)

    data['duration'] = data['duration'].fillna(0)

    if data.empty:
        raise ValueError("No valid plans provided for processing.")

    return data
