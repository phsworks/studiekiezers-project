from injector import Module, provider, singleton
from .extensions import db
from .users.service import UserService
from .auth.service import AuthService
from .groups.service import GroupService

class AppModule(Module):
    def __init__(self, app):
        self.app = app

    @provider
    @singleton
    def provide_user_service(self) -> UserService:
        return UserService(db)

    @provider
    @singleton
    def provide_auth_service(self) -> AuthService:
        return AuthService(db)

    @provider
    @singleton
    def provide_group_service(self) -> GroupService:   
        return GroupService(db)