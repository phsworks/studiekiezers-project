from flask import Blueprint, jsonify, request
from injector import inject
from .service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@inject
def login(auth_service: AuthService):
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'email and password are required'}), 400
    try:
        token, user = auth_service.login(data['email'], data['password'])
        return jsonify({'token': token, 'user': user.to_dict()}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/logout', methods=['POST'])
@inject
def logout(auth_service: AuthService):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401

    token = auth_header.split(' ')[1]
    auth_service.logout(token)
    return jsonify({'message': 'Logged out successfully'}), 200