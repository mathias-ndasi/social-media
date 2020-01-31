from flask import request, jsonify
from functools import wraps
import jwt

from app.models import User
from app.config import Config


# Token Required Decorator
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        error = None
        message = None
        success = False
        results = None
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            error = 'Token is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
        except:
            error = 'Token is Invalid'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), 401

        user = User.query.filter_by(
            id=data['user_id'], is_active=True, is_deleted=False, secret_code=None).first()

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        return f(*args, **kwargs)
    return wrapper


# Admin Required Decorator
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        error = None
        message = None
        success = False
        results = None
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            error = 'Token is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
        except:
            error = 'Token is Invalid'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), 401

        user = User.query.filter_by(
            id=data['user_id'], is_active=True, is_deleted=False, secret_code=None).first()

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        if not user.is_admin:
            message = 'Admin permissions required'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        return f(*args, **kwargs)
    return wrapper


# Get user from token
def get_user_from_token(*args, **kwargs):
    @wraps(f)
    def wrapper(*args, **kwargs):
        error = None
        message = None
        success = False
        results = None
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            error = 'Token is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
        except:
            error = 'Token is Invalid'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), 401

        user = User.query.filter_by(
            id=data['user_id'], is_active=True, is_deleted=False, secret_code=None).first()

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        return f(user, *args, **kwargs)
    return wrapper
