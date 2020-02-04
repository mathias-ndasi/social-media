from flask import request, jsonify
from functools import wraps
import datetime
import jwt

from app.config import Config
from app.models import User


# generate jwt token
def generate_token(user, *args, **kwargs):
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(days=2)}, Config.SECRET_KEY)
    return token.decode('UTF-8')


# verify jwt token
def token_verify(token, *args, **kwargs):
    error = None
    message = None
    success = False
    results = None

    try:
        data = jwt.decode(token, Config.SECRET_KEY)
    except Exception as e:
        error = 'Invalid token'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    try:
        user = User.query.filter_by(
            id=data['user_id'], is_active=True, is_deleted=False).first()
    except Exception as e:
        pass

    if not user:
        error = 'User not found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    return user
