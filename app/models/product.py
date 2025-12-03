"""
Product Model
=============
Handles all product-related database operations
"""

from app.models.database import Database
from mysql.connector import Error


class Product:
    """Product model for managing product data"""

    @staticmethod
    def get_all(page=1, per_page=10, search=None, category_id=None, supplier_id=None):
        """
        Get all products with pagination and filters

        Args:
            page (int): Page number
            per_page (int): Items per page
            search (str): Search term for product name or SKU
            category_id (int): Filter by category
            supplier_id (int): Filter by supplier

        Returns:
            dict: Products and pagination info
        """
        try:
            # Build WHERE clause
            where_conditions = []
            params = []

            if search:
                where_conditions.append("(p.product_name LIKE %s OR p.sku LIKE %s)")
                params.extend([f"%{search}%", f"%{search}%"])

            if category_id:
                where_conditions.append("p.category_id = %s")
                params.append(category_id)

            if supplier_id:
                where_conditions.append("p.supplier_id = %s")
                params.append(supplier_id)

            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

            # Count total records
            count_query = f"SELECT COUNT(*) as total FROM products p WHERE {where_clause}"
            total_result = Database.execute_query(count_query, tuple(params), fetch_one=True)
            total = total_result['total'] if total_result else 0

            # Get paginated data
            offset = (page - 1) * per_page
            query = f"""
                SELECT
                    p.product_id, p.product_name, p.sku, p.description,
                    p.category_id, c.category_name,
                    p.supplier_id, s.company_name as supplier_name,
                    p.unit_price, p.reorder_level,
                    COALESCE(i.quantity_in_stock, 0) as quantity_in_stock,
                    p.created_at, p.updated_at
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE {where_clause}
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
            """
            params.extend([per_page, offset])
            products = Database.execute_query(query, tuple(params))

            return {
                'success': True,
                'data': products,
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
    def get_by_id(product_id):
        """
        Get product by ID

        Args:
            product_id (int): Product ID

        Returns:
            dict: Product data
        """
        try:
            query = """
                SELECT
                    p.product_id, p.product_name, p.sku, p.description,
                    p.category_id, c.category_name,
                    p.supplier_id, s.company_name as supplier_name,
                    p.unit_price, p.reorder_level,
                    COALESCE(i.quantity_in_stock, 0) as quantity_in_stock,
                    i.warehouse_location,
                    p.created_at, p.updated_at
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.product_id = %s
            """
            product = Database.execute_query(query, (product_id,), fetch_one=True)

            if product:
                return {'success': True, 'data': product}
            else:
                return {'success': False, 'error': 'Product not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def create(data):
        """
        Create new product

        Args:
            data (dict): Product data

        Returns:
            dict: Created product with ID
        """
        try:
            query = """
                INSERT INTO products
                (product_name, sku, description, category_id, supplier_id, unit_price, reorder_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data['product_name'],
                data['sku'],
                data.get('description', ''),
                data['category_id'],
                data['supplier_id'],
                data['unit_price'],
                data.get('reorder_level', 10)
            )
            product_id = Database.execute_update(query, params)

            # Create initial inventory record with 0 stock
            inventory_query = """
                INSERT INTO inventory (product_id, quantity_in_stock, warehouse_location)
                VALUES (%s, 0, %s)
            """
            Database.execute_update(inventory_query, (product_id, data.get('warehouse_location', 'N/A')))

            return {
                'success': True,
                'message': 'Product created successfully',
                'product_id': product_id
            }
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def update(product_id, data):
        """
        Update product

        Args:
            product_id (int): Product ID
            data (dict): Updated product data

        Returns:
            dict: Success status
        """
        try:
            query = """
                UPDATE products
                SET product_name = %s, sku = %s, description = %s,
                    category_id = %s, supplier_id = %s,
                    unit_price = %s, reorder_level = %s
                WHERE product_id = %s
            """
            params = (
                data['product_name'],
                data['sku'],
                data.get('description', ''),
                data['category_id'],
                data['supplier_id'],
                data['unit_price'],
                data.get('reorder_level', 10),
                product_id
            )
            rows_affected = Database.execute_update(query, params)

            if rows_affected > 0:
                return {'success': True, 'message': 'Product updated successfully'}
            else:
                return {'success': False, 'error': 'Product not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def delete(product_id):
        """
        Delete product

        Args:
            product_id (int): Product ID

        Returns:
            dict: Success status
        """
        try:
            # Check if product has transactions
            check_query = "SELECT COUNT(*) as count FROM transactions WHERE product_id = %s"
            result = Database.execute_query(check_query, (product_id,), fetch_one=True)

            if result['count'] > 0:
                return {
                    'success': False,
                    'error': 'Cannot delete product with existing transactions'
                }

            query = "DELETE FROM products WHERE product_id = %s"
            rows_affected = Database.execute_update(query, (product_id,))

            if rows_affected > 0:
                return {'success': True, 'message': 'Product deleted successfully'}
            else:
                return {'success': False, 'error': 'Product not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_low_stock(threshold=None):
        """
        Get products with low stock

        Args:
            threshold (int): Custom threshold or use reorder_level

        Returns:
            dict: Low stock products
        """
        try:
            if threshold:
                query = """
                    SELECT
                        p.product_id, p.product_name, p.sku,
                        c.category_name, s.company_name as supplier_name,
                        i.quantity_in_stock, p.reorder_level, p.unit_price
                    FROM products p
                    INNER JOIN inventory i ON p.product_id = i.product_id
                    INNER JOIN categories c ON p.category_id = c.category_id
                    INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
                    WHERE i.quantity_in_stock <= %s
                    ORDER BY i.quantity_in_stock ASC
                """
                products = Database.execute_query(query, (threshold,))
            else:
                query = """
                    SELECT
                        p.product_id, p.product_name, p.sku,
                        c.category_name, s.company_name as supplier_name,
                        i.quantity_in_stock, p.reorder_level, p.unit_price
                    FROM products p
                    INNER JOIN inventory i ON p.product_id = i.product_id
                    INNER JOIN categories c ON p.category_id = c.category_id
                    INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
                    WHERE i.quantity_in_stock <= p.reorder_level
                    ORDER BY i.quantity_in_stock ASC
                """
                products = Database.execute_query(query)

            return {'success': True, 'data': products}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def check_sku_exists(sku, exclude_product_id=None):
        """
        Check if SKU already exists

        Args:
            sku (str): SKU to check
            exclude_product_id (int): Exclude this product ID from check

        Returns:
            bool: True if SKU exists
        """
        try:
            if exclude_product_id:
                query = "SELECT COUNT(*) as count FROM products WHERE sku = %s AND product_id != %s"
                result = Database.execute_query(query, (sku, exclude_product_id), fetch_one=True)
            else:
                query = "SELECT COUNT(*) as count FROM products WHERE sku = %s"
                result = Database.execute_query(query, (sku,), fetch_one=True)

            return result['count'] > 0
        except Error:
            return False
