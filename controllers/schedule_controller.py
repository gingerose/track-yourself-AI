
from flask import Blueprint, request, jsonify
from services.schedule_service import ScheduleService
from extensions import db

schedule_bp = Blueprint('schedule', __name__)
schedule_service = ScheduleService(db)

@schedule_bp.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    data = request.json
    user_id = data.get('user_id')
    date = data.get('date')

    if not user_id or not date:
        return jsonify({'error': 'Invalid input'}), 400

    result, error = schedule_service.generate_schedule(user_id, date)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(result), 200
