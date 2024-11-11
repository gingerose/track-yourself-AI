from flask import Blueprint, request, jsonify

from repositories.recommendation_repository import RecommendationRepository
from services.recommendation_service import RecommendationService
from extensions import db

recommendation_bp = Blueprint('recommendation', __name__)
recommendation_service = RecommendationService(db)

@recommendation_bp.route('/generate-recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    collection_id = data.get('collectionId')
    watched_ids = data.get('watchedIds')
    user_id = data.get('userId')

    if not collection_id or not watched_ids:
        return jsonify({'error': 'Invalid input'}), 400

    recommendations, error = recommendation_service.get_recommendations(collection_id, watched_ids, user_id)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(recommendations), 200

@recommendation_bp.route('/films-data', methods=['POST'])
def get_films_data():
    data = request.json
    collection_id = '2435466'  # ID фильмов
    limit = data.get('limit', 10)  # Устанавливаем 10 как значение по умолчанию
    offset = data.get('offset', 0)  # Начинаем с 0 как значение по умолчанию

    items, error = recommendation_service.get_items_from_collection(
        collection_id=collection_id,
        limit=limit,
        offset=offset
    )

    if error:
        return jsonify({'error': error}), 404

    return jsonify(items), 200


@recommendation_bp.route('/books-data', methods=['POST'])
def get_books_data():
    data = request.json
    collection_id = '9875768'  # ID книг
    limit = data.get('limit', 10)  # Устанавливаем 10 как значение по умолчанию
    offset = data.get('offset', 0)  # Начинаем с 0 как значение по умолчанию

    items, error = recommendation_service.get_items_from_collection(
        collection_id=collection_id,
        limit=limit,
        offset=offset
    )

    if error:
        return jsonify({'error': error}), 404

    return jsonify(items), 200


@recommendation_bp.route('/get-user-recommendations', methods=['POST'])
def get_user_recommendations():
    data = request.json
    collection_id = data.get('collectionId')
    user_id = data.get('userId')

    if not collection_id or not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    # Получаем рекомендации из базы данных
    recommendations = RecommendationRepository.get_recommendations_by_user_and_collection(collection_id, user_id)


    # Преобразуем данные в формат, который нужно вернуть
    recommendations_list = [{
        'id': recommendation.id,
        'collection_id': recommendation.collection_id,
        'user_id': recommendation.user_id,
        'recommendation_id': recommendation.recommendation_id,
        'title': recommendation.title,
        'image': recommendation.image
    } for recommendation in recommendations]

    return jsonify(recommendations_list), 200