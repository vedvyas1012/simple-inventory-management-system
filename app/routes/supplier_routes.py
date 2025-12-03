"""
Supplier Routes
===============
API endpoints for supplier management
"""

from flask import Blueprint, request, jsonify
from app.models.supplier import Supplier

supplier_bp = Blueprint('suppliers', __name__)


@supplier_bp.route('', methods=['GET'])
def get_suppliers():
    """GET /api/suppliers - Get all suppliers with pagination"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search')

        result = Supplier.get_all(page, per_page, search)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    """GET /api/suppliers/<id> - Get single supplier"""
    try:
        result = Supplier.get_by_id(supplier_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@supplier_bp.route('', methods=['POST'])
def create_supplier():
    """POST /api/suppliers - Create new supplier"""
    try:
        data = request.get_json()

        required_fields = ['company_name', 'contact_person', 'phone', 'email', 'address', 'city', 'state', 'postal_code']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = Supplier.create(data)
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    """PUT /api/suppliers/<id> - Update supplier"""
    try:
        data = request.get_json()

        required_fields = ['company_name', 'contact_person', 'phone', 'email', 'address', 'city', 'state', 'postal_code']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = Supplier.update(supplier_id, data)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    """DELETE /api/suppliers/<id> - Delete supplier"""
    try:
        result = Supplier.delete(supplier_id)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@supplier_bp.route('/<int:supplier_id>/products', methods=['GET'])
def get_supplier_products(supplier_id):
    """GET /api/suppliers/<id>/products - Get products by supplier"""
    try:
        result = Supplier.get_products(supplier_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
