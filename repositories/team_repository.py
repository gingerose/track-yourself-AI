from models.member import Member
from models.team import Team
from models.team_task import TeamTask
from models.user import User


class TeamRepository:
    def __init__(self, db):
        self.db = db

    def add_team_with_members(self, team_title, members_data):
        new_team = Team(title=team_title)
        self.db.session.add(new_team)
        self.db.session.flush()

        for member in members_data:
            user_id = member['userId']
            is_lead = member.get('isLead', False)
            new_member = Member(
                user_id=user_id,
                team_id=new_team.id,
                is_lead=is_lead
            )
            self.db.session.add(new_member)

        self.db.session.commit()
        return new_team

    def get_teams_by_user(self, user_id):
        team_ids = self.db.session.query(Member.team_id).filter(Member.user_id == user_id).distinct().all()
        team_ids = [team_id[0] for team_id in team_ids]

        if not team_ids:
            return []

        result = self.db.session.query(
            Member.id.label('member_id'),
            Member.is_lead,
            User.user_id,
            User.username,
            User.picture,
            Team.id.label('team_id'),
            Team.title
        ).join(User, Member.user_id == User.user_id) \
            .join(Team, Member.team_id == Team.id) \
            .filter(Member.team_id.in_(team_ids)) \
            .all()

        teams_dict = {}
        for row in result:
            team_id = row.team_id
            if team_id not in teams_dict:
                teams_dict[team_id] = {
                    'teamId': row.team_id,
                    'teamTitle': row.title,
                    'members': []
                }
            teams_dict[team_id]['members'].append({
                'memberId': row.member_id,
                'userId': row.user_id,
                'username': row.username,
                'picture': row.picture,
                'isLead': row.is_lead
            })

        return list(teams_dict.values())

    def delete_team(self, team_id):
        team = Team.query.get(team_id)
        if team:
            team = self.db.session.merge(team)
            self.db.session.delete(team)
            self.db.session.commit()
            return True
        return False

    def update_team_title(self, team_id, new_title):
        team = self.db.session.query(Team).filter_by(id=team_id).first()
        if team:
            team.title = new_title
            self.db.session.merge(team)
            self.db.session.commit()
            return team
        else:
            print("Team not found with ID:", team_id)
            return None

    def get_team_by_id(self, team_id):
        team = Team.query.filter_by(id=team_id).first()
        if not team:
            return None

        return {
            'teamId': team.id,
            'teamTitle': team.title,
        }

    def add_task(self, member_id, title, status='EMPTY'):
        task = TeamTask(
            member_id=member_id,
            title=title,
            status=status
        )
        self.db.session.add(task)
        self.db.session.commit()
        return task

    def get_tasks_by_team(self, team_id):

        tasks_data = self.db.session.query(
            Member.id.label('member_id'),
            User.username,
            User.picture,
            Member.is_lead,
            Member.comment.label('member_comment'),
            TeamTask.id.label('task_id'),
            TeamTask.title,
            TeamTask.date,
            TeamTask.status
        ).join(User, User.user_id == Member.user_id) \
            .outerjoin(TeamTask, TeamTask.member_id == Member.id) \
            .filter(Member.team_id == team_id) \
            .order_by(Member.id) \
            .all()

        members = {}
        for task in tasks_data:
            member_id = task.member_id
            if member_id not in members:
                members[member_id] = {
                    'memberId': member_id,
                    'username': task.username,
                    'picture': task.picture,
                    'isLead': task.is_lead,
                    'comment': task.member_comment,
                    'tasks': []
                }

            if task.task_id:
                members[member_id]['tasks'].append({
                    'taskId': task.task_id,
                    'title': task.title,
                    'date': task.date,
                    'status': task.status,
                })

        return list(members.values())

    def update_task(self, task_id, title=None, status=None):
        task = TeamTask.query.get(task_id)
        if task:
            if title:
                task.title = title
            if status:
                task.status = status
            self.db.session.merge(task)
            self.db.session.commit()
        return task

    def update_member(self, member_id, comment=None):
        member = Member.query.get(member_id)
        if member:
            if comment:
                member.comment = comment
            self.db.session.merge(member)
            self.db.session.commit()
        return member

    def delete_task(self, task_id):
        task = TeamTask.query.get(task_id)
        if task:
            task = self.db.session.merge(task)
            self.db.session.delete(task)
            self.db.session.commit()
        return task

    def get_all_users(self):
        return self.db.session.query(User.user_id, User.login, User.username, User.picture).all()
