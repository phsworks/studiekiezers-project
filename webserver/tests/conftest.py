import pytest
from unittest.mock import MagicMock, create_autospec
from injector import Module, provider, singleton
from app import create_app
from app.users.service import UserService
from app.auth.service import AuthService


@pytest.fixture(scope='session')
def services():
    """Create mock services once for the whole session."""
    return {
        'user': create_autospec(UserService, instance=True),
        'auth': create_autospec(AuthService, instance=True),
    }


@pytest.fixture(scope='session')
def client(services):
    mock_user_svc = services['user']
    mock_auth_svc = services['auth']

    class TestModule(Module):
        @provider
        @singleton
        def provide_user_service(self) -> UserService:
            return mock_user_svc

        @provider
        @singleton
        def provide_auth_service(self) -> AuthService:
            return mock_auth_svc

    app = create_app('app.config.TestConfig', injector_modules=[TestModule()])
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def reset_mocks(services):
    # clear before each test
    for svc in services.values():
        svc.reset_mock()
        # explicitly clear side_effect on every method
        for attr in dir(svc):
            try:
                method = getattr(svc, attr)
                if hasattr(method, 'side_effect'):
                    method.side_effect = None
                if hasattr(method, 'return_value'):
                    method.return_value = MagicMock()
            except Exception:
                pass
    yield


@pytest.fixture
def user_svc(services):
    return services['user']


@pytest.fixture
def auth_svc(services):
    return services['auth']


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.username = 'testuser'
    user.email = 'test@example.com'
    user.is_active = True
    user.to_dict.return_value = {
        'id': 1,
        'username': 'testuser',
        'email': 'test@example.com',
        'is_active': True,
        'created_at': None
    }
    return user