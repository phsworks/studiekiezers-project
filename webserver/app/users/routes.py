from flask import Blueprint, jsonify, request
from injector import inject
from .service import UserService

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@inject
def get_users(user_service: UserService):
    users = user_service.get_all()
    return jsonify([u.to_dict() for u in users]), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@inject
def get_user(user_id: int, user_service: UserService):
    user = user_service.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@users_bp.route('/', methods=['POST'])
@inject
def create_user(user_service: UserService):
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'username, email and password are required'}), 400
    try:
        user = user_service.create(data['username'], data['email'], data['password'])
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409

@users_bp.route('/<int:user_id>', methods=['PUT'])
@inject
def update_user(user_id: int, user_service: UserService):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    try:
        user = user_service.update(user_id, data)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@inject
def delete_user(user_id: int, user_service: UserService):
    try:
        user_service.delete(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404