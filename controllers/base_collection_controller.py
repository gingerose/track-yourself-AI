from flask import Blueprint, request, jsonify
from repositories.base_collection_item_repository import BaseCollectionItemRepository
from extensions import db

base_collection_item_bp = Blueprint('base_collection_item', __name__)

base_collection_item_repository = BaseCollectionItemRepository(db)

@base_collection_item_bp.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    collection_id = data.get('collectionId')
    user_id = data.get('userId')
    item_id = data.get('itemId')
    status = data.get('status')
    description = data.get('description')

    if not collection_id or not user_id or not item_id or not status or not description:
        return jsonify({'error': 'Invalid input'}), 400

    # Используем репозиторий для добавления айтема
    item = base_collection_item_repository.add_item(
        collection_id=collection_id,
        user_id=user_id,
        item_id=item_id,
        status=status,
        description=description
    )

    return jsonify({'message': 'Item added successfully', 'item': item.id}), 201


@base_collection_item_bp.route('/delete-item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    success = base_collection_item_repository.delete_item(item_id)
    if success:
        return jsonify({'message': 'Item deleted successfully'}), 200
    return jsonify({'error': 'Item not found'}), 404


@base_collection_item_bp.route('/get-items', methods=['POST'])
def get_items():
    data = request.json
    collection_id = data.get('collectionId')
    user_id = data.get('userId')

    if not collection_id or not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    items = base_collection_item_repository.get_items_by_user_and_collection(collection_id, user_id)

    items_list = [{'id': item.id, 'collection_id': item.collection_id, 'user_id': item.user_id, 'status': item.status,
                   'description': item.description} for item in items]

    return jsonify(items_list), 200

@base_collection_item_bp.route('/items-count', methods=['POST'])
def get_items_count():
    data = request.json
    collection_id = data.get('collectionId')
    user_id = data.get('userId')

    if not collection_id or not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    total_count, done_count = base_collection_item_repository.get_items_count_by_status(collection_id, user_id)

    return jsonify([done_count, total_count]), 200