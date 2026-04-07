import jwt
import datetime
from flask import current_app
from werkzeug.security import check_password_hash
from .models import TokenBlocklist
from app.users.models import User

class AuthService:
    def __init__(self, db):
        self.db = db

    def login(self, email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid email or password")

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return token, user

    def logout(self, token: str):
        blocked = TokenBlocklist(token=token)
        self.db.session.add(blocked)
        self.db.session.commit()

    def is_token_blocked(self, token: str):
        return TokenBlocklist.query.filter_by(token=token).first() is not None

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")