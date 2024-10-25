from flask import Blueprint, request, jsonify
from services.recommendation_service import RecommendationService

recommendation_bp = Blueprint('recommendation', __name__)
recommendation_service = RecommendationService()

@recommendation_bp.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    collection_id = data.get('collection_id')
    watched_ids = data.get('watched_ids')

    if not collection_id or not watched_ids:
        return jsonify({'error': 'Invalid input'}), 400

    recommendations, error = recommendation_service.get_recommendations(collection_id, watched_ids)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(recommendations), 200
