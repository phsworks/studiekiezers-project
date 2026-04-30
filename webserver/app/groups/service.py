from .models import Group, Lap, Feedback

class GroupService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return Group.query.all()

    def get_by_id(self, group_id: int):
        return Group.query.get(group_id)

    def create(self, group_name: str, member_1: str, member_2: str = None):
        if Group.query.filter_by(group_name=group_name).first():
            raise ValueError(f"Group {group_name} already exists")
        group = Group(group_name=group_name, member_1=member_1, member_2=member_2)
        self.db.session.add(group)
        self.db.session.commit()
        return group

    def add_lap(self, group_id: int, lap_time: float):
        group = self.get_by_id(group_id)
        if not group:
            raise ValueError(f"Group {group_id} not found")
        lap = Lap(group_id=group_id, lap_time=lap_time)
        self.db.session.add(lap)
        self.db.session.commit()
        return lap

    def add_feedback(self, group_id: int, rating: int, comment: str = None):
        group = self.get_by_id(group_id)
        if not group:
            raise ValueError(f"Group {group_id} not found")
        feedback = Feedback(group_id=group_id, rating=rating, comment=comment)
        self.db.session.add(feedback)
        self.db.session.commit()
        return feedback