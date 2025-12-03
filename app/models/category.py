"""
Category Model
==============
Handles all category-related database operations
"""

from app.models.database import Database
from mysql.connector import Error


class Category:
    """Category model for managing category data"""

    @staticmethod
    def get_all():
        """Get all categories"""
        try:
            query = """
                SELECT
                    c.*,
                    COUNT(p.product_id) as product_count
                FROM categories c
                LEFT JOIN products p ON c.category_id = p.category_id
                GROUP BY c.category_id
                ORDER BY c.category_name
            """
            categories = Database.execute_query(query)
            return {'success': True, 'data': categories}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_by_id(category_id):
        """Get category by ID"""
        try:
            query = "SELECT * FROM categories WHERE category_id = %s"
            category = Database.execute_query(query, (category_id,), fetch_one=True)

            if category:
                return {'success': True, 'data': category}
            else:
                return {'success': False, 'error': 'Category not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def create(data):
        """Create new category"""
        try:
            query = """
                INSERT INTO categories (category_name, description)
                VALUES (%s, %s)
            """
            params = (data['category_name'], data.get('description', ''))
            category_id = Database.execute_update(query, params)

            return {
                'success': True,
                'message': 'Category created successfully',
                'category_id': category_id
            }
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def update(category_id, data):
        """Update category"""
        try:
            query = """
                UPDATE categories
                SET category_name = %s, description = %s
                WHERE category_id = %s
            """
            params = (data['category_name'], data.get('description', ''), category_id)
            rows_affected = Database.execute_update(query, params)

            if rows_affected > 0:
                return {'success': True, 'message': 'Category updated successfully'}
            else:
                return {'success': False, 'error': 'Category not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def delete(category_id):
        """Delete category"""
        try:
            # Check if category has products
            check_query = "SELECT COUNT(*) as count FROM products WHERE category_id = %s"
            result = Database.execute_query(check_query, (category_id,), fetch_one=True)

            if result['count'] > 0:
                return {
                    'success': False,
                    'error': 'Cannot delete category with existing products'
                }

            query = "DELETE FROM categories WHERE category_id = %s"
            rows_affected = Database.execute_update(query, (category_id,))

            if rows_affected > 0:
                return {'success': True, 'message': 'Category deleted successfully'}
            else:
                return {'success': False, 'error': 'Category not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}
