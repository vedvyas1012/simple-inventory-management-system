"""
Authentication Routes
=====================
API endpoints for user authentication and management
"""

from flask import Blueprint, request, jsonify
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """POST /api/auth/login - User login"""
    try:
        data = request.get_json()

        if 'username' not in data or 'password' not in data:
            return jsonify({'success': False, 'error': 'Missing username or password'}), 400

        result = User.authenticate(data['username'], data['password'])
        return jsonify(result), 200 if result['success'] else 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """POST /api/auth/verify - Verify JWT token"""
    try:
        data = request.get_json()

        if 'token' not in data:
            return jsonify({'success': False, 'error': 'Missing token'}), 400

        payload = User.verify_token(data['token'])

        if payload:
            return jsonify({'success': True, 'data': payload}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/users', methods=['GET'])
def get_users():
    """GET /api/auth/users - Get all users (admin only)"""
    try:
        result = User.get_all()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """GET /api/auth/users/<id> - Get user by ID"""
    try:
        result = User.get_by_id(user_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/users', methods=['POST'])
def create_user():
    """POST /api/auth/users - Create new user (admin only)"""
    try:
        data = request.get_json()

        required_fields = ['username', 'password', 'full_name', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = User.create(data)
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT /api/auth/users/<id> - Update user (admin only)"""
    try:
        data = request.get_json()

        required_fields = ['full_name', 'email', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = User.update(user_id, data)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """POST /api/auth/change-password - Change user password"""
    try:
        data = request.get_json()

        required_fields = ['user_id', 'old_password', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = User.change_password(data['user_id'], data['old_password'], data['new_password'])
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/users/<int:user_id>/toggle-active', methods=['PUT'])
def toggle_user_active(user_id):
    """PUT /api/auth/users/<id>/toggle-active - Toggle user active status (admin only)"""
    try:
        result = User.toggle_active(user_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
