"""
Database Utility Module
========================
Manages database connections and provides utility functions
"""

import mysql.connector
from mysql.connector import pooling, Error
from app.config import Config
from contextlib import contextmanager


class Database:
    """Database connection manager with connection pooling"""

    _connection_pool = None

    @classmethod
    def get_connection_pool(cls):
        """
        Get or create connection pool

        Returns:
            PooledMySQLConnection: Database connection pool
        """
        if cls._connection_pool is None:
            try:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="inventory_pool",
                    pool_size=5,
                    pool_reset_session=True,
                    **Config.DB_CONFIG
                )
                print("✓ Database connection pool created successfully")
            except Error as e:
                print(f"✗ Error creating connection pool: {e}")
                raise

        return cls._connection_pool

    @classmethod
    def get_connection(cls):
        """
        Get a connection from the pool

        Returns:
            PooledMySQLConnection: Database connection
        """
        try:
            pool = cls.get_connection_pool()
            connection = pool.get_connection()
            return connection
        except Error as e:
            print(f"✗ Error getting connection: {e}")
            raise

    @classmethod
    @contextmanager
    def get_cursor(cls, dictionary=True, buffered=True):
        """
        Context manager for database cursor with automatic connection management

        Args:
            dictionary (bool): Return results as dictionaries
            buffered (bool): Use buffered cursor

        Yields:
            cursor: Database cursor
        """
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=dictionary, buffered=buffered)
            yield cursor
            connection.commit()
        except Error as e:
            if connection:
                connection.rollback()
            print(f"✗ Database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False):
        """
        Execute a SELECT query and return results

        Args:
            query (str): SQL query
            params (tuple): Query parameters
            fetch_one (bool): Return single row instead of all rows

        Returns:
            dict or list: Query results
        """
        with cls.get_cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    @classmethod
    def execute_update(cls, query, params=None):
        """
        Execute INSERT, UPDATE, or DELETE query

        Args:
            query (str): SQL query
            params (tuple): Query parameters

        Returns:
            int: Last inserted ID or rows affected
        """
        with cls.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid or cursor.rowcount

    @classmethod
    def execute_many(cls, query, params_list):
        """
        Execute query with multiple parameter sets

        Args:
            query (str): SQL query
            params_list (list): List of parameter tuples

        Returns:
            int: Rows affected
        """
        with cls.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

    @classmethod
    def call_procedure(cls, proc_name, params=None):
        """
        Call a stored procedure

        Args:
            proc_name (str): Procedure name
            params (tuple): Procedure parameters

        Returns:
            list: Results from procedure
        """
        with cls.get_cursor() as cursor:
            cursor.callproc(proc_name, params or ())
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            return results

    @classmethod
    def test_connection(cls):
        """
        Test database connection

        Returns:
            bool: True if connection successful
        """
        try:
            with cls.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Error as e:
            print(f"✗ Connection test failed: {e}")
            return False


def init_db():
    """
    Initialize database connection
    This function is called when the app starts
    """
    try:
        if Database.test_connection():
            print("✓ Database connection successful")
            return True
        else:
            print("✗ Database connection failed")
            return False
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        return False


# Utility functions for common operations
def paginate_query(query, page=1, per_page=10):
    """
    Add pagination to SQL query

    Args:
        query (str): Base SQL query
        page (int): Page number (1-indexed)
        per_page (int): Items per page

    Returns:
        str: Query with LIMIT and OFFSET
    """
    offset = (page - 1) * per_page
    return f"{query} LIMIT {per_page} OFFSET {offset}"


def build_search_condition(search_term, columns):
    """
    Build SQL LIKE condition for multiple columns

    Args:
        search_term (str): Search term
        columns (list): List of column names

    Returns:
        tuple: (condition_string, params)
    """
    if not search_term or not columns:
        return "", ()

    conditions = " OR ".join([f"{col} LIKE %s" for col in columns])
    params = tuple([f"%{search_term}%" for _ in columns])
    return f"({conditions})", params


def format_datetime(dt):
    """
    Format datetime for database

    Args:
        dt: datetime object

    Returns:
        str: Formatted datetime string
    """
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return None
