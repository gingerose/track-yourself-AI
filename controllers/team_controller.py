from flask import Blueprint, request, jsonify
from repositories.team_repository import TeamRepository
from extensions import db

team_bp = Blueprint('team', __name__)
team_repository = TeamRepository(db)

# 1. Добавление новой команды с участниками
@team_bp.route('/team', methods=['POST'])
def add_team_with_members():
    data = request.json
    team_title = data.get('teamTitle')
    members_data = data.get('members')

    # Body
    # teamTitle
    # user_id = member['userId']
    # is_lead = member.get('isLead', False)

    if not team_title or not members_data:
        return jsonify({'error': 'Invalid input'}), 400

    new_team = team_repository.add_team_with_members(team_title, members_data)
    return jsonify({'teamId': new_team.id, 'teamTitle': new_team.title}), 201

# 2. Получение информации о команде и её участниках
@team_bp.route('/team/<int:user_id>/members', methods=['GET'])
def get_team_members(user_id):
    members = team_repository.get_teams_by_user(user_id)
    if not members:
        return jsonify({'error': 'Team not found or no members'}), 404

    return jsonify(members), 200

# 3. Удаление команды
@team_bp.route('/team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    print("!!!!!")
    rows_deleted = team_repository.delete_team(team_id)
    print(rows_deleted)
    if not rows_deleted:
        return jsonify({'error': 'Team not found'}), 404

    return jsonify({'message': 'Team deleted successfully'}), 200

# 4. Обновление названия команды
@team_bp.route('/team/<int:team_id>', methods=['PUT'])
def update_team_title(team_id):
    data = request.json
    new_title = data.get('teamTitle')

    if not new_title:
        return jsonify({'error': 'New team title is required'}), 400

    updated_team = team_repository.update_team_title(team_id, new_title)
    if not updated_team:
        return jsonify({'error': 'Team not found'}), 404

    return jsonify({'teamId': updated_team.id, 'teamTitle': updated_team.title}), 200

# 5. Получение информации о команде по ID
@team_bp.route('/team/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    team = team_repository.get_team_by_id(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404

    return jsonify(team), 200

# 6. Добавление нового задания для участника команды
@team_bp.route('/task', methods=['POST'])
def add_task():
    data = request.json
    member_id = data.get('memberId')
    title = data.get('title')
    comment = data.get('comment')
    status = data.get('status', 'EMPTY')

    if not member_id or not title:
        return jsonify({'error': 'Member ID and title are required'}), 400

    task = team_repository.add_task(member_id, title, comment, status)
    return jsonify({'taskId': task.id, 'title': task.title, 'comment': task.comment, 'status': task.status}), 201

# 7. Получение всех заданий для определённой команды
@team_bp.route('/team/tasks/<int:team_id>', methods=['GET'])
def get_tasks_by_team(team_id):
    tasks = team_repository.get_tasks_by_team(team_id)
    result = [
        {
            'taskId': task.id,
            'title': task.title,
            'date': task.date,
            'comment': task.comment,
            'status': task.status,
            'username': username,
            'picture': picture,
            'isLead': is_lead,
            'memberId': id
        }
        for task, username, picture, is_lead, id in tasks
    ]
    return jsonify(result), 200

# 8. Обновление задания
@team_bp.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    title = data.get('title')
    comment = data.get('comment')
    status = data.get('status')

    task = team_repository.update_task(task_id, title, comment, status)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task updated successfully'}), 200

# 9. Удаление задания
@team_bp.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = team_repository.delete_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task deleted successfully'}), 200

@team_bp.route('/users', methods=['GET'])
def get_all_users():
    users = team_repository.get_all_users()

    users_list = [
        {
            'userId': user.user_id,
            'login': user.login,
            'username': user.username,
            'picture': user.picture
        } for user in users
    ]

    return jsonify(users_list), 200