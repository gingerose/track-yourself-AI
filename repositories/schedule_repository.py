from extensions import db
from models.plan import Plan
from models.schedule import Schedule


class ScheduleRepository:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def add_schedule(plan_id, date, day_of_week, suggested_time):
        schedule = Schedule(plan_id=plan_id, date=date, day_of_week=day_of_week, suggested_time=suggested_time)
        db.session.add(schedule)
        db.session.commit()
        return schedule

    @staticmethod
    def get_schedule_by_date(date, user_id):
        return Schedule.query.join(Plan, Schedule.plan_id == Plan.plan_id) \
            .filter(Schedule.date == date, Plan.user_id == user_id) \
            .all()

    @staticmethod
    def delete_schedule_by_date(date_value, user_id):
        schedules = Schedule.query.join(Plan, Schedule.plan_id == Plan.plan_id) \
            .filter(Schedule.date == date_value, Plan.user_id == user_id) \
            .all()
        if schedules:
            for schedule in schedules:
                schedule = db.session.merge(schedule)
                db.session.delete(schedule)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_plans_with_schedule(date, user_id, days_of_week=None):
        query = db.session.query(
            Plan.plan_id,
            Plan.user_id,
            Plan.status,
            Plan.name,
            Plan.priority,
            Plan.deadline,
            Plan.duration,
            Schedule.day_of_week,
            Schedule.suggested_time
        ).join(Schedule, Plan.plan_id == Schedule.plan_id) \
            .filter(Schedule.date == date, Plan.user_id == user_id, Plan.status != "DONE", Plan.status != "NOT_ACTUAL") \
            .order_by(Schedule.day_of_week)

        results = query.all()

        result_dicts = [
            {
                "planId": row.plan_id,
                "userId": row.user_id,
                "status": row.status,
                "name": row.name,
                "priority": row.priority,
                "deadline": row.deadline,
                "dayOfWeek": row.day_of_week,
                "duration": row.duration,
                "suggestedTime": row.suggested_time,
            }
            for row in results
        ]
        return result_dicts


