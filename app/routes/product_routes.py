"""
Product Routes
==============
API endpoints for product management
"""

from flask import Blueprint, request, jsonify
from app.models.product import Product

product_bp = Blueprint('products', __name__)


@product_bp.route('', methods=['GET'])
def get_products():
    """
    GET /api/products
    Get all products with pagination, search, and filters
    Query params: page, per_page, search, category_id, supplier_id
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search')
        category_id = request.args.get('category_id', type=int)
        supplier_id = request.args.get('supplier_id', type=int)

        result = Product.get_all(page, per_page, search, category_id, supplier_id)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    GET /api/products/<id>
    Get single product by ID
    """
    try:
        result = Product.get_by_id(product_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('', methods=['POST'])
def create_product():
    """
    POST /api/products
    Create new product
    Request body: product_name, sku, description, category_id, supplier_id, unit_price, reorder_level
    """
    try:
        data = request.get_json()

        # Validation
        required_fields = ['product_name', 'sku', 'category_id', 'supplier_id', 'unit_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        # Check if SKU already exists
        if Product.check_sku_exists(data['sku']):
            return jsonify({'success': False, 'error': 'SKU already exists'}), 400

        result = Product.create(data)
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    PUT /api/products/<id>
    Update product
    Request body: product_name, sku, description, category_id, supplier_id, unit_price, reorder_level
    """
    try:
        data = request.get_json()

        # Validation
        required_fields = ['product_name', 'sku', 'category_id', 'supplier_id', 'unit_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        # Check if SKU already exists (excluding current product)
        if Product.check_sku_exists(data['sku'], product_id):
            return jsonify({'success': False, 'error': 'SKU already exists'}), 400

        result = Product.update(product_id, data)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    DELETE /api/products/<id>
    Delete product
    """
    try:
        result = Product.delete(product_id)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@product_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    """
    GET /api/products/low-stock
    Get products below reorder level
    Query params: threshold (optional)
    """
    try:
        threshold = request.args.get('threshold', type=int)
        result = Product.get_low_stock(threshold)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
