from models.plan import Plan


class PlanRepository:
    def __init__(self, db):
        self.db = db

    def get_plans_by_user_before_date(self, user_id, date):
        return Plan.query.filter(Plan.user_id == user_id, Plan.deadline <= date).all()

    def update_plan_decomposition(self, plan_id, decomposition):
        plan = Plan.query.filter_by(plan_id=plan_id).first()
        if not plan:
            return None

        print(plan.decomposition)
        plan.decomposition = decomposition
        print(plan.decomposition)
        self.db.session.commit()

        return plan