from extensions import db
from datetime import datetime


class Plan(db.Model):
    __tablename__ = 'plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String)
    creation_date = db.Column(db.Date, default=datetime.utcnow)
    day_of_week = db.Column(db.Integer)
    priority = db.Column(db.String)
    modify_date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)
    deadline = db.Column(db.Date)
