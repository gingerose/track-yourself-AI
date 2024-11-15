from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TeamTask(db.Model):
    __tablename__ = 'team_tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=datetime.today, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String, default='EMPTY', nullable=False)