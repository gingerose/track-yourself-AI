from flask import Blueprint, request, jsonify
from services.decomposition_service import Decompose_task
from extensions import db

decomposition_bp = Blueprint('decomposition', __name__)
#decomposition_service = DecompositionService(api_key='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')  # Замените на ваш API-ключ

@decomposition_bp.route('/decompose-task', methods=['POST'])
def decompose_task():
    data = request.json
    task_description = data.get('task_description')

    if not task_description:
        return jsonify({'error': 'Invalid input'}), 400

    steps, error = Decompose_task(task_description)

    if error:
        return jsonify({'error': error}), 500

    return jsonify({'steps': steps}), 200
