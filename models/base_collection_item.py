from extensions import db


class BaseCollectionItem(db.Model):
    __tablename__ = 'base_collection_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
