from app.extensions import db

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), unique=True, nullable=False)
    member_1 = db.Column(db.String(100), nullable=False)
    member_2 = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    laps = db.relationship('Lap', backref='group', lazy=True)
    feedbacks = db.relationship('Feedback', backref='group', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'member_1': self.member_1,
            'member_2': self.member_2,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Lap(db.Model):
    __tablename__ = 'laps'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    lap_time = db.Column(db.Float, nullable=False)
    driven_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'lap_time': self.lap_time,
            'driven_at': self.driven_at.isoformat() if self.driven_at else None
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    given_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'rating': self.rating,
            'comment': self.comment,
            'given_at': self.given_at.isoformat() if self.given_at else None
        }



    