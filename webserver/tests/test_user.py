def test_get_users_empty(client, user_svc):
    user_svc.get_all.return_value = []
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json == []

def test_get_users_returns_list(client, user_svc, mock_user):
    user_svc.get_all.return_value = [mock_user]
    response = client.get('/users/')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['username'] == 'testuser'

def test_get_user_not_found(client, user_svc):
    user_svc.get_by_id.return_value = None
    response = client.get('/users/999')
    assert response.status_code == 404

def test_get_user_found(client, user_svc, mock_user):
    user_svc.get_by_id.return_value = mock_user
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'

def test_create_user_missing_fields(client, user_svc):
    response = client.post('/users/', json={'email': 'x@x.com'})
    assert response.status_code == 400

def test_create_user_conflict(client, user_svc):
    user_svc.create.side_effect = ValueError("Email already registered")
    response = client.post('/users/', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 409

def test_create_user_success(client, user_svc, mock_user):
    user_svc.create.return_value = mock_user
    response = client.post('/users/', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'

def test_delete_user_not_found(client, user_svc):
    user_svc.delete.side_effect = ValueError("User not found")
    response = client.delete('/users/999')
    assert response.status_code == 404

def test_delete_user_success(client, user_svc):
    user_svc.delete.return_value = None
    response = client.delete('/users/1')
    assert response.status_code == 200