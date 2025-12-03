"""
Supplier Model
==============
Handles all supplier-related database operations
"""

from app.models.database import Database
from mysql.connector import Error


class Supplier:
    """Supplier model for managing supplier data"""

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        """
        Get all suppliers with pagination

        Args:
            page (int): Page number
            per_page (int): Items per page
            search (str): Search term

        Returns:
            dict: Suppliers and pagination info
        """
        try:
            where_clause = "1=1"
            params = []

            if search:
                where_clause = "(company_name LIKE %s OR contact_person LIKE %s OR city LIKE %s)"
                params = [f"%{search}%", f"%{search}%", f"%{search}%"]

            # Count total
            count_query = f"SELECT COUNT(*) as total FROM suppliers WHERE {where_clause}"
            total_result = Database.execute_query(count_query, tuple(params), fetch_one=True)
            total = total_result['total'] if total_result else 0

            # Get paginated data
            offset = (page - 1) * per_page
            query = f"""
                SELECT * FROM suppliers
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            params.extend([per_page, offset])
            suppliers = Database.execute_query(query, tuple(params))

            return {
                'success': True,
                'data': suppliers,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_by_id(supplier_id):
        """Get supplier by ID"""
        try:
            query = "SELECT * FROM suppliers WHERE supplier_id = %s"
            supplier = Database.execute_query(query, (supplier_id,), fetch_one=True)

            if supplier:
                return {'success': True, 'data': supplier}
            else:
                return {'success': False, 'error': 'Supplier not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def create(data):
        """Create new supplier"""
        try:
            query = """
                INSERT INTO suppliers
                (company_name, contact_person, phone, email, address, city, state, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data['company_name'],
                data['contact_person'],
                data['phone'],
                data['email'],
                data['address'],
                data['city'],
                data['state'],
                data['postal_code']
            )
            supplier_id = Database.execute_update(query, params)

            return {
                'success': True,
                'message': 'Supplier created successfully',
                'supplier_id': supplier_id
            }
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def update(supplier_id, data):
        """Update supplier"""
        try:
            query = """
                UPDATE suppliers
                SET company_name = %s, contact_person = %s, phone = %s,
                    email = %s, address = %s, city = %s, state = %s, postal_code = %s
                WHERE supplier_id = %s
            """
            params = (
                data['company_name'],
                data['contact_person'],
                data['phone'],
                data['email'],
                data['address'],
                data['city'],
                data['state'],
                data['postal_code'],
                supplier_id
            )
            rows_affected = Database.execute_update(query, params)

            if rows_affected > 0:
                return {'success': True, 'message': 'Supplier updated successfully'}
            else:
                return {'success': False, 'error': 'Supplier not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def delete(supplier_id):
        """Delete supplier"""
        try:
            # Check if supplier has products
            check_query = "SELECT COUNT(*) as count FROM products WHERE supplier_id = %s"
            result = Database.execute_query(check_query, (supplier_id,), fetch_one=True)

            if result['count'] > 0:
                return {
                    'success': False,
                    'error': 'Cannot delete supplier with existing products'
                }

            query = "DELETE FROM suppliers WHERE supplier_id = %s"
            rows_affected = Database.execute_update(query, (supplier_id,))

            if rows_affected > 0:
                return {'success': True, 'message': 'Supplier deleted successfully'}
            else:
                return {'success': False, 'error': 'Supplier not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_products(supplier_id):
        """Get all products from a supplier"""
        try:
            query = """
                SELECT
                    p.product_id, p.product_name, p.sku,
                    c.category_name, p.unit_price,
                    COALESCE(i.quantity_in_stock, 0) as quantity_in_stock
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.supplier_id = %s
                ORDER BY p.product_name
            """
            products = Database.execute_query(query, (supplier_id,))
            return {'success': True, 'data': products}
        except Error as e:
            return {'success': False, 'error': str(e)}
