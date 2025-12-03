"""
Transaction Model
=================
Handles all transaction-related database operations
"""

from app.models.database import Database
from mysql.connector import Error
from datetime import datetime


class Transaction:
    """Transaction model for managing stock transactions"""

    @staticmethod
    def get_all(page=1, per_page=10, product_id=None, transaction_type=None, start_date=None, end_date=None):
        """
        Get all transactions with filters

        Args:
            page (int): Page number
            per_page (int): Items per page
            product_id (int): Filter by product
            transaction_type (str): Filter by type
            start_date (str): Start date filter
            end_date (str): End date filter

        Returns:
            dict: Transactions and pagination info
        """
        try:
            where_conditions = []
            params = []

            if product_id:
                where_conditions.append("t.product_id = %s")
                params.append(product_id)

            if transaction_type:
                where_conditions.append("t.transaction_type = %s")
                params.append(transaction_type)

            if start_date:
                where_conditions.append("DATE(t.transaction_date) >= %s")
                params.append(start_date)

            if end_date:
                where_conditions.append("DATE(t.transaction_date) <= %s")
                params.append(end_date)

            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

            # Count total
            count_query = f"SELECT COUNT(*) as total FROM transactions t WHERE {where_clause}"
            total_result = Database.execute_query(count_query, tuple(params), fetch_one=True)
            total = total_result['total'] if total_result else 0

            # Get paginated data
            offset = (page - 1) * per_page
            query = f"""
                SELECT
                    t.transaction_id, t.product_id,
                    p.product_name, p.sku,
                    t.transaction_type, t.quantity,
                    t.transaction_date, t.reference_number,
                    t.remarks, t.created_by,
                    (t.quantity * p.unit_price) as transaction_value
                FROM transactions t
                INNER JOIN products p ON t.product_id = p.product_id
                WHERE {where_clause}
                ORDER BY t.transaction_date DESC
                LIMIT %s OFFSET %s
            """
            params.extend([per_page, offset])
            transactions = Database.execute_query(query, tuple(params))

            return {
                'success': True,
                'data': transactions,
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
    def get_by_product(product_id, start_date=None, end_date=None):
        """Get transaction history for a product"""
        try:
            where_conditions = ["t.product_id = %s"]
            params = [product_id]

            if start_date:
                where_conditions.append("DATE(t.transaction_date) >= %s")
                params.append(start_date)

            if end_date:
                where_conditions.append("DATE(t.transaction_date) <= %s")
                params.append(end_date)

            where_clause = " AND ".join(where_conditions)

            query = f"""
                SELECT
                    t.transaction_id, t.transaction_type, t.quantity,
                    t.transaction_date, t.reference_number,
                    t.remarks, t.created_by,
                    p.product_name, p.sku
                FROM transactions t
                INNER JOIN products p ON t.product_id = p.product_id
                WHERE {where_clause}
                ORDER BY t.transaction_date DESC
            """
            transactions = Database.execute_query(query, tuple(params))
            return {'success': True, 'data': transactions}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def record_stock_in(product_id, quantity, reference_number, remarks, created_by):
        """
        Record stock in transaction using stored procedure

        Args:
            product_id (int): Product ID
            quantity (int): Quantity to add
            reference_number (str): PO/reference number
            remarks (str): Additional notes
            created_by (str): Username

        Returns:
            dict: Success status with transaction ID
        """
        try:
            # Call stored procedure
            results = Database.call_procedure(
                'sp_record_stock_in',
                (product_id, quantity, reference_number, remarks, created_by)
            )

            if results and 'success_message' in results[0]:
                return {
                    'success': True,
                    'message': results[0]['success_message'],
                    'transaction_id': results[0].get('transaction_id')
                }
            else:
                return {'success': False, 'error': 'Failed to record stock in'}
        except Error as e:
            error_msg = str(e)
            if 'Error:' in error_msg:
                return {'success': False, 'error': error_msg.split('Error:')[1].strip()}
            return {'success': False, 'error': error_msg}

    @staticmethod
    def record_stock_out(product_id, quantity, reference_number, remarks, created_by):
        """
        Record stock out transaction using stored procedure

        Args:
            product_id (int): Product ID
            quantity (int): Quantity to remove
            reference_number (str): Invoice/order number
            remarks (str): Additional notes
            created_by (str): Username

        Returns:
            dict: Success status with transaction ID
        """
        try:
            # Call stored procedure
            results = Database.call_procedure(
                'sp_record_stock_out',
                (product_id, quantity, reference_number, remarks, created_by)
            )

            if results and 'success_message' in results[0]:
                return {
                    'success': True,
                    'message': results[0]['success_message'],
                    'transaction_id': results[0].get('transaction_id'),
                    'remaining_stock': results[0].get('remaining_stock')
                }
            else:
                return {'success': False, 'error': 'Failed to record stock out'}
        except Error as e:
            error_msg = str(e)
            if 'Error:' in error_msg:
                return {'success': False, 'error': error_msg.split('Error:')[1].strip()}
            return {'success': False, 'error': error_msg}

    @staticmethod
    def adjust_stock(product_id, new_quantity, remarks, created_by):
        """
        Adjust stock quantity using stored procedure

        Args:
            product_id (int): Product ID
            new_quantity (int): New stock quantity
            remarks (str): Reason for adjustment
            created_by (str): Username

        Returns:
            dict: Success status
        """
        try:
            # Call stored procedure
            results = Database.call_procedure(
                'sp_adjust_stock',
                (product_id, new_quantity, remarks, created_by)
            )

            if results and 'success_message' in results[0]:
                return {
                    'success': True,
                    'message': results[0]['success_message'],
                    'transaction_id': results[0].get('transaction_id')
                }
            else:
                return {'success': False, 'error': 'Failed to adjust stock'}
        except Error as e:
            error_msg = str(e)
            if 'Error:' in error_msg:
                return {'success': False, 'error': error_msg.split('Error:')[1].strip()}
            return {'success': False, 'error': error_msg}

    @staticmethod
    def get_summary(start_date=None, end_date=None):
        """
        Get transaction summary

        Args:
            start_date (str): Start date
            end_date (str): End date

        Returns:
            dict: Transaction summary by type
        """
        try:
            where_conditions = []
            params = []

            if start_date:
                where_conditions.append("DATE(t.transaction_date) >= %s")
                params.append(start_date)

            if end_date:
                where_conditions.append("DATE(t.transaction_date) <= %s")
                params.append(end_date)

            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

            query = f"""
                SELECT
                    t.transaction_type,
                    COUNT(*) as transaction_count,
                    SUM(t.quantity) as total_quantity,
                    SUM(t.quantity * p.unit_price) as total_value
                FROM transactions t
                INNER JOIN products p ON t.product_id = p.product_id
                WHERE {where_clause}
                GROUP BY t.transaction_type
                ORDER BY t.transaction_type
            """
            summary = Database.execute_query(query, tuple(params))
            return {'success': True, 'data': summary}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_recent_transactions(limit=10):
        """Get recent transactions"""
        try:
            query = """
                SELECT
                    t.transaction_id, t.product_id,
                    p.product_name, p.sku,
                    t.transaction_type, t.quantity,
                    t.transaction_date, t.created_by
                FROM transactions t
                INNER JOIN products p ON t.product_id = p.product_id
                ORDER BY t.transaction_date DESC
                LIMIT %s
            """
            transactions = Database.execute_query(query, (limit,))
            return {'success': True, 'data': transactions}
        except Error as e:
            return {'success': False, 'error': str(e)}
