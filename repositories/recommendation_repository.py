from extensions import db
from models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def add_or_update_recommendation(collection_id, user_id, recommendation_id, title, image=None):
        recommendation = Recommendation.query.filter_by(
            collection_id=collection_id,
            user_id=user_id,
            recommendation_id=recommendation_id
        ).first()

        if recommendation:
            recommendation.title = title
            recommendation.image = image
        else:
            recommendation = Recommendation(
                collection_id=collection_id,
                user_id=user_id,
                recommendation_id=recommendation_id,
                title=title,
                image=image
            )
            db.session.add(recommendation)

        db.session.commit()
        return recommendation

    @staticmethod
    def get_recommendations_by_user_and_collection(collection_id, user_id):
        recommendations = Recommendation.query.filter_by(
            collection_id=collection_id,
            user_id=user_id
        ).all()

        return recommendations
