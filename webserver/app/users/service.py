from werkzeug.security import generate_password_hash
from .models import User

class UserService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id: int):
        return User.query.get(user_id)

    def get_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def create(self, username: str, email: str, password: str):
        if User.query.filter_by(email=email).first():
            raise ValueError(f"Email {email} is already registered")
        if User.query.filter_by(username=username).first():
            raise ValueError(f"Username {username} is already taken")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def update(self, user_id: int, data: dict):
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])

        self.db.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        self.db.session.delete(user)
        self.db.session.commit()