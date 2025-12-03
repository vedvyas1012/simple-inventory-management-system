"""
Transaction Routes
==================
API endpoints for transaction management
"""

from flask import Blueprint, request, jsonify
from app.models.transaction import Transaction

transaction_bp = Blueprint('transactions', __name__)


@transaction_bp.route('', methods=['GET'])
def get_transactions():
    """GET /api/transactions - Get all transactions with filters"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        product_id = request.args.get('product_id', type=int)
        transaction_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        result = Transaction.get_all(page, per_page, product_id, transaction_type, start_date, end_date)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transaction_bp.route('/history/<int:product_id>', methods=['GET'])
def get_product_history(product_id):
    """GET /api/transactions/history/<product_id> - Get transaction history for product"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        result = Transaction.get_by_product(product_id, start_date, end_date)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transaction_bp.route('/stock-in', methods=['POST'])
def stock_in():
    """POST /api/transactions/stock-in - Record stock in transaction"""
    try:
        data = request.get_json()

        required_fields = ['product_id', 'quantity', 'created_by']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = Transaction.record_stock_in(
            data['product_id'],
            data['quantity'],
            data.get('reference_number', ''),
            data.get('remarks', ''),
            data['created_by']
        )
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transaction_bp.route('/stock-out', methods=['POST'])
def stock_out():
    """POST /api/transactions/stock-out - Record stock out transaction"""
    try:
        data = request.get_json()

        required_fields = ['product_id', 'quantity', 'created_by']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = Transaction.record_stock_out(
            data['product_id'],
            data['quantity'],
            data.get('reference_number', ''),
            data.get('remarks', ''),
            data['created_by']
        )
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transaction_bp.route('/adjust', methods=['POST'])
def adjust_stock():
    """POST /api/transactions/adjust - Adjust stock quantity"""
    try:
        data = request.get_json()

        required_fields = ['product_id', 'new_quantity', 'created_by']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        result = Transaction.adjust_stock(
            data['product_id'],
            data['new_quantity'],
            data.get('remarks', ''),
            data['created_by']
        )
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transaction_bp.route('/summary', methods=['GET'])
def get_transaction_summary():
    """GET /api/transactions/summary - Get transaction summary"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        result = Transaction.get_summary(start_date, end_date)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transaction_bp.route('/recent', methods=['GET'])
def get_recent_transactions():
    """GET /api/transactions/recent - Get recent transactions"""
    try:
        limit = int(request.args.get('limit', 10))
        result = Transaction.get_recent_transactions(limit)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
