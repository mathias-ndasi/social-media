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

        try:
            user = User.query.filter_by(
                id=data['user_id'], is_active=True, is_deleted=False, secret_code=None).first()

            if not user:
                error = 'Token is Invalid'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            pass

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

        try:
            user = User.query.filter_by(
                id=data['user_id'], is_active=True, is_admin=True, is_deleted=False, secret_code=None).first()

            if not user:
                error = 'Admin permissions required'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            pass

        return f(*args, **kwargs)
    return wrapper


# Get user from token
def get_user_from_token(f):
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

        try:
            user = User.query.filter_by(
                id=data['user_id'], is_active=True, is_deleted=False, secret_code=None).first()

            if not user:
                error = 'Admin permissions required'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            pass

        return f(user, *args, **kwargs)
    return wrapper
