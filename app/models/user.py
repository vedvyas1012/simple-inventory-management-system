"""
User Model
==========
Handles all user-related database operations
"""

from app.models.database import Database
from mysql.connector import Error
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.config import Config


class User:
    """User model for authentication and user management"""

    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, password_hash):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def generate_token(user_id, username, role):
        """
        Generate JWT token

        Args:
            user_id (int): User ID
            username (str): Username
            role (str): User role

        Returns:
            str: JWT token
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """
        Verify JWT token

        Args:
            token (str): JWT token

        Returns:
            dict: Decoded token payload or None
        """
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user

        Args:
            username (str): Username
            password (str): Password

        Returns:
            dict: User data with token if successful
        """
        try:
            query = """
                SELECT user_id, username, password_hash, full_name, email, role, is_active
                FROM users
                WHERE username = %s
            """
            user = Database.execute_query(query, (username,), fetch_one=True)

            if not user:
                return {'success': False, 'error': 'Invalid username or password'}

            if not user['is_active']:
                return {'success': False, 'error': 'Account is inactive'}

            if not User.verify_password(password, user['password_hash']):
                return {'success': False, 'error': 'Invalid username or password'}

            # Generate token
            token = User.generate_token(user['user_id'], user['username'], user['role'])

            # Remove password hash from response
            del user['password_hash']

            return {
                'success': True,
                'message': 'Login successful',
                'user': user,
                'token': token
            }
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_all():
        """Get all users"""
        try:
            query = """
                SELECT user_id, username, full_name, email, role, created_at, is_active
                FROM users
                ORDER BY created_at DESC
            """
            users = Database.execute_query(query)
            return {'success': True, 'data': users}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            query = """
                SELECT user_id, username, full_name, email, role, created_at, is_active
                FROM users
                WHERE user_id = %s
            """
            user = Database.execute_query(query, (user_id,), fetch_one=True)

            if user:
                return {'success': True, 'data': user}
            else:
                return {'success': False, 'error': 'User not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def create(data):
        """Create new user"""
        try:
            # Hash password
            password_hash = User.hash_password(data['password'])

            query = """
                INSERT INTO users (username, password_hash, full_name, email, role)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                data['username'],
                password_hash,
                data['full_name'],
                data['email'],
                data.get('role', 'staff')
            )
            user_id = Database.execute_update(query, params)

            return {
                'success': True,
                'message': 'User created successfully',
                'user_id': user_id
            }
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def update(user_id, data):
        """Update user (excluding password)"""
        try:
            query = """
                UPDATE users
                SET full_name = %s, email = %s, role = %s
                WHERE user_id = %s
            """
            params = (data['full_name'], data['email'], data['role'], user_id)
            rows_affected = Database.execute_update(query, params)

            if rows_affected > 0:
                return {'success': True, 'message': 'User updated successfully'}
            else:
                return {'success': False, 'error': 'User not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        try:
            # Get current password hash
            query = "SELECT password_hash FROM users WHERE user_id = %s"
            result = Database.execute_query(query, (user_id,), fetch_one=True)

            if not result:
                return {'success': False, 'error': 'User not found'}

            # Verify old password
            if not User.verify_password(old_password, result['password_hash']):
                return {'success': False, 'error': 'Invalid current password'}

            # Hash new password
            new_password_hash = User.hash_password(new_password)

            # Update password
            update_query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
            Database.execute_update(update_query, (new_password_hash, user_id))

            return {'success': True, 'message': 'Password changed successfully'}
        except Error as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def toggle_active(user_id):
        """Toggle user active status"""
        try:
            query = "UPDATE users SET is_active = NOT is_active WHERE user_id = %s"
            rows_affected = Database.execute_update(query, (user_id,))

            if rows_affected > 0:
                return {'success': True, 'message': 'User status updated'}
            else:
                return {'success': False, 'error': 'User not found'}
        except Error as e:
            return {'success': False, 'error': str(e)}
