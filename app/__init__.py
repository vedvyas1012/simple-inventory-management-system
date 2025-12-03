"""
Application Factory
===================
Creates and configures the Flask application
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os


def create_app(config_name='default'):
    """
    Application factory function
    Creates and configures Flask application instance

    Args:
        config_name (str): Configuration name (development, production, testing)

    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app instance
    app = Flask(__name__)

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Enable CORS
    CORS(app)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Create database tables if they don't exist
    # (In production, use migrations instead)
    with app.app_context():
        from app.models.database import init_db
        init_db()

    return app


def register_blueprints(app):
    """Register all application blueprints"""

    from app.routes.product_routes import product_bp
    from app.routes.supplier_routes import supplier_bp
    from app.routes.category_routes import category_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.report_routes import report_bp
    from app.routes.auth_routes import auth_bp

    # Register API blueprints
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(supplier_bp, url_prefix='/api/suppliers')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Register main routes (for serving HTML pages)
    register_main_routes(app)


def register_main_routes(app):
    """Register main application routes for serving HTML pages"""

    @app.route('/')
    def index():
        """Landing page - redirects to login or dashboard"""
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        """Dashboard page"""
        return render_template('dashboard.html')

    @app.route('/products')
    def products_page():
        """Products management page"""
        return render_template('products/list.html')

    @app.route('/suppliers')
    def suppliers_page():
        """Suppliers management page"""
        return render_template('suppliers/list.html')

    @app.route('/categories')
    def categories_page():
        """Categories management page"""
        return render_template('categories/list.html')

    @app.route('/inventory')
    def inventory_page():
        """Inventory management page"""
        return render_template('inventory/list.html')

    @app.route('/transactions')
    def transactions_page():
        """Transaction history page"""
        return render_template('transactions/list.html')

    @app.route('/reports')
    def reports_page():
        """Reports page"""
        return render_template('reports/dashboard.html')


def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'message': str(error)
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'message': str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 errors"""
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
