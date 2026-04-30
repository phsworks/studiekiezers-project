from flask import Blueprint, jsonify, request
from injector import inject
from .service import GroupService

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/', methods=['GET'])
@inject
def get_groups(group_service: GroupService):
    groups = group_service.get_all()
    return jsonify([g.to_dict() for g in groups]), 200

@groups_bp.route('/', methods=['POST'])
@inject
def create_group(group_service: GroupService):
    data = request.get_json()
    if not data or 'group_name' not in data or 'member_1' not in data:
        return jsonify({'error': 'group_name and member_1 are required'}), 400
    try:
        group = group_service.create(data['group_name'], data['member_1'], data.get('member_2'))
        return jsonify(group.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409

@groups_bp.route('/<int:group_id>/laps', methods=['POST'])
@inject
def add_lap(group_id: int, group_service: GroupService):
    data = request.get_json()
    if not data or 'lap_time' not in data:
        return jsonify({'error': 'lap_time is required'}), 400
    try:
        lap = group_service.add_lap(group_id, data['lap_time'])
        return jsonify(lap.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@groups_bp.route('/<int:group_id>/feedback', methods=['POST'])
@inject
def add_feedback(group_id: int, group_service: GroupService):
    data = request.get_json()
    if not data or 'rating' not in data:
        return jsonify({'error': 'rating is required'}), 400
    try:
        feedback = group_service.add_feedback(group_id, data['rating'], data.get('comment'))
        return jsonify(feedback.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404