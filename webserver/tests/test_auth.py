from unittest.mock import MagicMock

def test_login_missing_fields(client, auth_svc):
    response = client.post('/auth/login', json={'email': 'x@x.com'})
    assert response.status_code == 400

def test_login_invalid_credentials(client, auth_svc):
    auth_svc.login.side_effect = ValueError("Invalid email or password")
    response = client.post('/auth/login', json={
        'email': 'bad@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_login_success(client, auth_svc):
    mock_user = MagicMock()
    mock_user.to_dict.return_value = {'id': 1, 'username': 'testuser'}
    auth_svc.login.return_value = ('mock.jwt.token', mock_user)
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json['token'] == 'mock.jwt.token'

def test_logout_missing_header(client, auth_svc):
    response = client.post('/auth/logout')
    assert response.status_code == 401

def test_logout_success(client, auth_svc):
    auth_svc.logout.return_value = None
    response = client.post('/auth/logout', headers={
        'Authorization': 'Bearer mock.jwt.token'
    })
    assert response.status_code == 200