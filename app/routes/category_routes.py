"""
Category Routes
===============
API endpoints for category management
"""

from flask import Blueprint, request, jsonify
from app.models.category import Category

category_bp = Blueprint('categories', __name__)


@category_bp.route('', methods=['GET'])
def get_categories():
    """GET /api/categories - Get all categories"""
    try:
        result = Category.get_all()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """GET /api/categories/<id> - Get single category"""
    try:
        result = Category.get_by_id(category_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('', methods=['POST'])
def create_category():
    """POST /api/categories - Create new category"""
    try:
        data = request.get_json()

        if 'category_name' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: category_name'}), 400

        result = Category.create(data)
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """PUT /api/categories/<id> - Update category"""
    try:
        data = request.get_json()

        if 'category_name' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: category_name'}), 400

        result = Category.update(category_id, data)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """DELETE /api/categories/<id> - Delete category"""
    try:
        result = Category.delete(category_id)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
