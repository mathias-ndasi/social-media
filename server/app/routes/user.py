from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from app import models, db
from app.config import Config
from app.utils import util, email
from app.schemas import schema_user
from app.auth import token, decorators

account = Blueprint('account', __name__, url_prefix='/account')


@account.route('/signup', methods=['POST'])
def signup():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        data = request.get_json()

        if not data:
            error = 'Json data is required'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            clean_data = schema_user.user_schema.load(data)

            users = models.User.query.all()
            for user in users:
                if user.email == clean_data['email'] or user.username == clean_data['username']:
                    error = 'User already exist'
                    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            password = clean_data['password']
            hash_pwd = util.hash_password(password)

            new_user = models.User(
                username=clean_data['username'], email=clean_data['email'], password=hash_pwd)
            email.account_comfirmation_email(new_user)

            success = True
            message = 'Account activation code sent to your email'

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = 'Only Json data is accepted'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/account_confirmation', methods=['PUT'])
def account_confirm():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        if not data:
            error = {'secret_code': 'This is a required field'}
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        secret_code = data['secret_code']

        user = models.User.query.filter_by(
            secret_code=secret_code, is_active=False, is_deleted=False).first()

        if not user:
            error = 'Invalid secret code or user already activated'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        user.is_active = True
        user.secret_code = None
        db.session.commit()
        message = 'User account is activated, you can now login'
        success = True

    else:
        error = 'Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/login', methods=['POST'])
def login():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            clean_data = schema_user.login_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], is_active=True, is_deleted=False, secret_code=None).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            if not util.verify_password(user, clean_data['password']):
                error = 'Incorrect password'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            user_token = token.generate_token(user)
            message = 'User successfully login'
            success = True
            results = schema_user.user_schema.dump(user)
            results['token'] = user_token

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/user/<string:username>', methods=['GET'])
@decorators.token_required
def get_single_user(username):
    error = None
    message = None
    success = False
    results = None

    user = models.User.query.filter_by(
        username=username, is_active=True, is_deleted=False, secret_code=None).first()

    if not user:
        error = 'User not found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    success = True
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/users', methods=['GET'])
@decorators.token_required
def get_all_users():
    error = None
    message = None
    success = False
    results = None

    users = models.User.query.filter_by(
        is_active=True, is_deleted=False, secret_code=None).all()

    if not users:
        error = 'User not found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    success = True
    results = schema_user.user_schemas.dump(users)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/<string:username>/profile_pic', methods=['PUT'])
@decorators.token_required
def update_profile_pic(username):
    error = None
    message = None
    success = False
    results = None

    if not request.files:
        error = 'Form data is required'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    if len(request.files) > 1:
        error = 'Only a single image can be updated'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    if not request.files['profile_pic']:
        error = {'profile_pic': 'This is a required field'}
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    user = models.User.query.filter_by(
        username=username, is_active=True, is_deleted=False, secret_code=None).first()

    if not user:
        error = 'Invalid user'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    file = request.files['profile_pic']
    picture_path = util.save_picture(file, user)

    if picture_path == None:
        error = 'Invalid file extension'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    user.profile_pic = picture_path
    db.session.commit()

    success = True
    message = 'Profile pic successfully updated'
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/admin/<string:username>', methods=['PUT'])
# @decorators.token_required
@decorators.admin_required
def register_admin(username):
    error = None
    message = None
    success = False
    results = None

    user = models.User.query.filter_by(
        username=username, is_active=True, is_deleted=False, secret_code=None).first()

    if not user:
        error = 'User not found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    user.is_admin = True
    user.is_active = True
    db.session.commit()

    success = True
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/delete/<string:username>', methods=['DELETE'])
@decorators.token_required
@decorators.admin_required
def delete_user(username):
    error = None
    message = None
    success = False
    results = None

    user = models.User.query.filter_by(
        username=username, is_active=True, is_deleted=False).first()

    if not user:
        error = 'User not found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

    user.is_deleted = True
    user.is_active = False

    db.session.commit()

    success = True
    message = 'User successfully deleted'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/user/update/<string:username>/bio', methods=['PUT'])
@decorators.token_required
def update_user_bio(username):
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            clean_data = schema_user.user_bio_schema.load(data)

            user = models.User.query.filter_by(
                username=username, is_active=True, is_deleted=False, secret_code=None).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            if clean_data.get('bio'):
                user.bio = clean_data['bio']

            if clean_data.get('location'):
                user.location = clean_data['location']

            if clean_data.get('website'):
                user.website = clean_data['website']

            db.session.commit()

            message = 'User bio successfully updated'
            success = True
            results = schema_user.user_schema.dump(user)

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/password_reset', methods=['POST'])
def password_reset():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            clean_data = schema_user.user_email_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], is_active=True, is_deleted=False).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            email.password_reset_email(user)

            message = 'Check your email for password reset secret code'
            success = True

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/password_reset_code_validation', methods=['PUT'])
def password_reset_code_validation():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        if not data.get('secret_code'):
            error = {'secret_code': 'This is a required field'}
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            user = models.User.query.filter_by(
                secret_code=data['secret_code'], is_active=True, is_deleted=False).first()
        except Exception as e:
            pass

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        user.secret_code = None
        db.session.commit()

        message = 'Secret code valid'
        success = True

    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/password_reset_confirm', methods=['PUT'])
def password_reset_confirm():
    error = None
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            clean_data = schema_user.user_password_change_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], is_active=True, is_deleted=False).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            user.password = util.hash_password(clean_data['password'])

            db.session.commit()

            message = 'User password successfully updated, you can now login'
            success = True

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@account.route('/test')
def test():
    print('HERE.......................')
    return jsonify({'message': 'WORKING'})
