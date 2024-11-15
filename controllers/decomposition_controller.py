from flask import Blueprint, request, jsonify
from services.decomposition_service import DecompositionService
from extensions import db

decomposition_bp = Blueprint('decomposition', __name__)
decomposition_service = DecompositionService(db)

@decomposition_bp.route('/decompose-task', methods=['POST'])
def decompose_task():
    data = request.json

    planId = data.get('planId')
    task_description = data.get('name')

    if not task_description:
        return jsonify({'error': 'Invalid input'}), 400

    steps, error = decomposition_service.decompose_task(task_description, planId)
    print(error)

    if error:
        return jsonify({'error': error}), 500

    return jsonify(steps), 200
