"""
Inventory Model
===============
Handles all inventory-related database operations
"""

from app.models.database import Database
from mysql.connector import Error


class Inventory:
    """Inventory model for managing stock levels"""

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        """Get all inventory with pagination"""
        try:
            where_clause = "1=1"
            params = []

            if search:
                where_clause = "(p.product_name LIKE %s OR p.sku LIKE %s)"
                params = [f"%{search}%", f"%{search}%"]

            # Count total
            count_query = f"""
                SELECT COUNT(*) as total
                FROM inventory i
                INNER JOIN products p ON i.product_id = p.product_id
                WHERE {where_clause}
            """
            total_result = Database.execute_query(count_query, tuple(params), fetch_one=True)
            total = total_result['total'] if total_result else 0

            # Get paginated data
            offset = (page - 1) * per_page
            query = f"""
                SELECT
                    i.inventory_id, i.product_id,
                    p.product_name, p.sku,
                    c.category_name, s.company_name as supplier_name,
                    i.quantity_in_stock, p.reorder_level,
                    i.warehouse_location, p.unit_price,
                    (i.quantity_in_stock * p.unit_price) as stock_value,
                    i.last_updated
                FROM inventory i
                INNER JOIN products p ON i.product_id = p.product_id
                INNER JOIN categories c ON p.category_id = c.category_id
                INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE {where_clause}
                ORDER BY p.product_name
                LIMIT %s OFFSET %s
            """
            params.extend([per_page, offset])
            inventory = Database.execute_query(query, tuple(params))

            return {
                'success': True,
                'data': inventory,
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
    def get_by_product_id(product_id):
        """Get inventory for a specific product"""
        try:
            query = """
                SELECT
                    i.inventory_id, i.product_id,
                    p.product_name, p.sku,
                    i.quantity_in_stock, p.reorder_level,
                    i.warehouse_location, p.unit_price,
                    (i.quantity_in_stock * p.unit_price) as stock_value,
                    i.last_updated
                FROM inventory i
                INNER JOIN products p ON i.product_id = p.product_id
                WHERE i.product_id = %s
            """
            inventory = Database.execute_query(query, (product_id,), fetch_one=True)

            if inventory:
                return {'success': True, 'data': inventory}
            else:
                return {'success': False, 'error': 'Inventory not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def update_quantity(product_id, new_quantity, warehouse_location=None):
        """
        Update stock quantity directly

        Args:
            product_id (int): Product ID
            new_quantity (int): New stock quantity
            warehouse_location (str): Warehouse location

        Returns:
            dict: Success status
        """
        try:
            if new_quantity < 0:
                return {'success': False, 'error': 'Quantity cannot be negative'}

            if warehouse_location:
                query = """
                    UPDATE inventory
                    SET quantity_in_stock = %s, warehouse_location = %s
                    WHERE product_id = %s
                """
                params = (new_quantity, warehouse_location, product_id)
            else:
                query = """
                    UPDATE inventory
                    SET quantity_in_stock = %s
                    WHERE product_id = %s
                """
                params = (new_quantity, product_id)

            rows_affected = Database.execute_update(query, params)

            if rows_affected > 0:
                return {'success': True, 'message': 'Inventory updated successfully'}
            else:
                return {'success': False, 'error': 'Inventory not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_stock_summary():
        """Get summary statistics for inventory"""
        try:
            query = """
                SELECT
                    COUNT(DISTINCT i.product_id) as total_products,
                    SUM(i.quantity_in_stock) as total_units,
                    SUM(i.quantity_in_stock * p.unit_price) as total_value,
                    COUNT(CASE WHEN i.quantity_in_stock <= p.reorder_level THEN 1 END) as low_stock_count,
                    COUNT(CASE WHEN i.quantity_in_stock = 0 THEN 1 END) as out_of_stock_count
                FROM inventory i
                INNER JOIN products p ON i.product_id = p.product_id
            """
            summary = Database.execute_query(query, fetch_one=True)
            return {'success': True, 'data': summary}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_by_category():
        """Get inventory grouped by category"""
        try:
            query = """
                SELECT
                    c.category_id,
                    c.category_name,
                    COUNT(p.product_id) as product_count,
                    SUM(i.quantity_in_stock) as total_units,
                    SUM(i.quantity_in_stock * p.unit_price) as total_value
                FROM categories c
                LEFT JOIN products p ON c.category_id = p.category_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                GROUP BY c.category_id, c.category_name
                ORDER BY total_value DESC
            """
            categories = Database.execute_query(query)
            return {'success': True, 'data': categories}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_by_supplier():
        """Get inventory grouped by supplier"""
        try:
            query = """
                SELECT
                    s.supplier_id,
                    s.company_name,
                    COUNT(p.product_id) as product_count,
                    SUM(i.quantity_in_stock) as total_units,
                    SUM(i.quantity_in_stock * p.unit_price) as total_value
                FROM suppliers s
                LEFT JOIN products p ON s.supplier_id = p.supplier_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                GROUP BY s.supplier_id, s.company_name
                ORDER BY total_value DESC
            """
            suppliers = Database.execute_query(query)
            return {'success': True, 'data': suppliers}
        except Error as e:
            return {'success': False, 'error': str(e)}
