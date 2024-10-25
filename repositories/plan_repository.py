from models.plan import Plan


class PlanRepository:
    def __init__(self, db):
        self.db = db

    def get_plans_by_user_before_date(self, user_id, date):
        return Plan.query.filter(Plan.user_id == user_id, Plan.creation_date <= date).all()
