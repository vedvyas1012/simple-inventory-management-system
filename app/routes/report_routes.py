"""
Report Routes
=============
API endpoints for reports and analytics
"""

from flask import Blueprint, request, jsonify
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.transaction import Transaction

report_bp = Blueprint('reports', __name__)


@report_bp.route('/stock-summary', methods=['GET'])
def stock_summary():
    """GET /api/reports/stock-summary - Current stock summary"""
    try:
        result = Inventory.get_stock_summary()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/low-stock', methods=['GET'])
def low_stock():
    """GET /api/reports/low-stock - Low stock report"""
    try:
        threshold = request.args.get('threshold', type=int)
        result = Product.get_low_stock(threshold)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/transaction-summary', methods=['GET'])
def transaction_summary():
    """GET /api/reports/transaction-summary - Transaction summary by date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        result = Transaction.get_summary(start_date, end_date)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/category-wise', methods=['GET'])
def category_wise():
    """GET /api/reports/category-wise - Products grouped by category"""
    try:
        result = Inventory.get_by_category()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/supplier-wise', methods=['GET'])
def supplier_wise():
    """GET /api/reports/supplier-wise - Products grouped by supplier"""
    try:
        result = Inventory.get_by_supplier()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@report_bp.route('/dashboard-stats', methods=['GET'])
def dashboard_stats():
    """GET /api/reports/dashboard-stats - Dashboard statistics"""
    try:
        # Get stock summary
        stock_summary = Inventory.get_stock_summary()

        # Get low stock products count
        low_stock = Product.get_low_stock()

        # Get recent transactions
        recent_transactions = Transaction.get_recent_transactions(5)

        # Combine all stats
        if stock_summary['success'] and low_stock['success'] and recent_transactions['success']:
            return jsonify({
                'success': True,
                'data': {
                    'stock_summary': stock_summary['data'],
                    'low_stock_count': len(low_stock['data']),
                    'recent_transactions': recent_transactions['data']
                }
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch dashboard stats'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
