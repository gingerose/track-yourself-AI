from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Recommendation(db.Model):
    __tablename__ = 'recommendation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    recommendation_id = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=False)
