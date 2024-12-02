from datetime import timedelta, datetime

from repositories.plan_repository import PlanRepository
from repositories.schedule_repository import ScheduleRepository
from utils.lstm_model import predict_schedule


class ScheduleService:
    def __init__(self, db):
        self.plan_repo = PlanRepository(db)
        self.schedule_repo = ScheduleRepository(db)

    def get_schedule_by_date(self, user_id, date_str):
        week_start = self.get_week_start(date_str)
        week_end = week_start + timedelta(days=6)
        return self.schedule_repo.get_plans_with_schedule(week_end, user_id)

    def get_week_start(self, date_str):
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
        return date - timedelta(days=date.weekday())

    def generate_week_schedule(self, user_id, date_str):
        week_start = self.get_week_start(date_str)
        week_end = week_start + timedelta(days=6)

        plans = self.plan_repo.get_plans_by_user_before_date(user_id, week_end)

        if not plans:
            return None, "No plans found for the user."

        schedule_predictions = predict_schedule(plans, week_end)
        schedule_predictions = {str(k): v for k, v in schedule_predictions.items()}

        schedule = self.schedule_repo.get_schedule_by_date(week_end, user_id)
        if schedule:
            self.schedule_repo.delete_schedule_by_date(week_end, user_id)

        for day, schedules in schedule_predictions.items():
            for schedule_data in schedules:
                plan_id = schedule_data['plan_id']
                date = week_end
                day_of_week = day
                self.schedule_repo.add_schedule(plan_id, date, day_of_week, schedule_data['suggested_time'])

        return self.schedule_repo.get_plans_with_schedule(week_end, user_id), None

