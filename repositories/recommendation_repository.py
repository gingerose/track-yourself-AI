from extensions import db
from models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def delete_recommendations(collection_id, user_id):
        print(f"Deleting recommendations where collection_id={collection_id} and user_id={user_id}")

        query = f"DELETE FROM recommendation WHERE collection_id = {collection_id} AND user_id = {user_id}"

        result = db.session.execute(query)

        db.session.commit()

        print(f"Rows deleted: {result.rowcount}")

        db.session.close()

        if db.session.is_active:
            print("Session is still active.")
        else:
            print("Session is closed.")

        return result.rowcount

    @staticmethod
    def add_recommendations(collection_id, user_id, recommendation_id, title, image=None):
        recommendation = Recommendation(
            collection_id=collection_id,
            user_id=user_id,
            recommendation_id=recommendation_id,
            title=title,
            image=image
        )
        db.session.add(recommendation)
        db.session.commit()

    @staticmethod
    def get_recommendations_by_user_and_collection(collection_id, user_id):
        recommendations = Recommendation.query.filter_by(
            collection_id=collection_id,
            user_id=user_id
        ).all()

        return recommendations
