
from flask import Blueprint, request, jsonify
from services.schedule_service import ScheduleService
from extensions import db

schedule_bp = Blueprint('schedule', __name__)
schedule_service = ScheduleService(db)

@schedule_bp.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    user_id = data.get('userId')
    date = data.get('date')

    if not user_id or not date:
        return jsonify({'error': 'Invalid input'}), 400

    result, error = schedule_service.generate_week_schedule(user_id, date)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(result), 200

@schedule_bp.route('/get-schedule', methods=['POST'])
def get_schedule():
    data = request.json
    user_id = data.get('userId')
    date = data.get('date')

    if not user_id or not date:
        return jsonify({'error': 'Invalid input'}), 400

    result = schedule_service.get_schedule_by_date(user_id, date)

    return jsonify(result), 200
