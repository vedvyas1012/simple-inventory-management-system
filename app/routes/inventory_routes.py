"""
Inventory Routes
================
API endpoints for inventory management
"""

from flask import Blueprint, request, jsonify
from app.models.inventory import Inventory

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('', methods=['GET'])
def get_inventory():
    """GET /api/inventory - Get all inventory with pagination"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search')

        result = Inventory.get_all(page, per_page, search)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@inventory_bp.route('/<int:product_id>', methods=['GET'])
def get_inventory_by_product(product_id):
    """GET /api/inventory/<product_id> - Get inventory for product"""
    try:
        result = Inventory.get_by_product_id(product_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@inventory_bp.route('/<int:product_id>', methods=['PUT'])
def update_inventory(product_id):
    """PUT /api/inventory/<product_id> - Update stock quantity"""
    try:
        data = request.get_json()

        if 'quantity' not in data:
            return jsonify({'success': False, 'error': 'Missing required field: quantity'}), 400

        result = Inventory.update_quantity(
            product_id,
            data['quantity'],
            data.get('warehouse_location')
        )
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@inventory_bp.route('/summary', methods=['GET'])
def get_inventory_summary():
    """GET /api/inventory/summary - Get inventory summary statistics"""
    try:
        result = Inventory.get_stock_summary()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@inventory_bp.route('/by-category', methods=['GET'])
def get_inventory_by_category():
    """GET /api/inventory/by-category - Get inventory grouped by category"""
    try:
        result = Inventory.get_by_category()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@inventory_bp.route('/by-supplier', methods=['GET'])
def get_inventory_by_supplier():
    """GET /api/inventory/by-supplier - Get inventory grouped by supplier"""
    try:
        result = Inventory.get_by_supplier()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
