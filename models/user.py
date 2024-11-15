from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=False)