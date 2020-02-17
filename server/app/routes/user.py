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
    error = {'username': None, 'email': None, 'password': None}
    message = None
    success = False
    results = None

    if request.is_json:
        data = request.get_json()

        if not data:
            error['username'] = 'Json data is required'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_schema.load(data)

            users = models.User.query.all()
            for user in users:
                if user.email == clean_data['email'] or user.username == clean_data['username']:
                    error['username'] = 'User already exist'
                    error['email'] = 'User already exist'
                    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            password = clean_data['password']
            hash_pwd = util.hash_password(password)

            new_user = models.User(
                username=clean_data['username'], email=clean_data['email'], password=hash_pwd)
            email.account_comfirmation_email(new_user)

            success = True
            message = 'Account activation code sent to your email'

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('CREATED')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error['username'] = 'Only Json data is accepted'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/account_confirmation', methods=['PUT'])
def account_confirm():
    error = {'secret_code': None}
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error['secret_code'] = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error['secret_code'] = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        if not data:
            error['secret_code'] = 'This is a required field'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        secret_code = data['secret_code']

        user = models.User.query.filter_by(
            secret_code=secret_code, is_active=False, is_deleted=False).first()

        if not user:
            error['secret_code'] = 'Invalid secret code or user already activated'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        user.is_active = True
        user.secret_code = None
        db.session.commit()
        message = 'User account is activated, you can now login'
        success = True

        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

    else:
        error['secret_code'] = 'Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/login', methods=['POST'])
def login():
    error = {'email': None, 'password': None}
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error['email'] = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error['email'] = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.login_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], is_active=True, is_deleted=False, secret_code=None).first()

            if not user:
                error['email'] = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            if not util.verify_password(user, clean_data['password']):
                error['password'] = 'Incorrect password'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            user_token = token.generate_token(user)
            message = 'User successfully login'
            success = True
            results = schema_user.user_schema.dump(user)
            results['token'] = user_token

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error['password'] = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


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
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    success = True
    results = schema_user.user_schema.dump(user)
    results['notifications'] = []

    for notification in user.notifications:
        data = {'body': notification.body, 'created_by': notification.created_by,
                'notification_date': notification.notification_date}
        results['notifications'].append(data)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')


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
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    success = True
    results = schema_user.user_schemas.dump(users)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')


@account.route('/<string:username>/profile_pic', methods=['PUT'])
@decorators.token_required
def update_profile_pic(username):
    error = {'profile_pic': None}
    message = None
    success = False
    results = None

    if not request.files:
        error['profile_pic'] = 'Form data is required'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    if len(request.files) > 1:
        error['profile_pic'] = 'Only a single image can be updated'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    if not request.files['profile_pic']:
        error['profile_pic'] = 'This is a required field'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    user = models.User.query.filter_by(
        username=username, is_active=True, is_deleted=False, secret_code=None).first()

    if not user:
        error['profile_pic'] = 'Invalid user'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    file = request.files['profile_pic']
    picture_path = util.save_picture(file, user)

    if picture_path == None:
        error['profile_pic'] = 'Invalid file extension'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    user.profile_pic = picture_path
    db.session.commit()

    success = True
    message = 'Profile pic successfully updated'
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')


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
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    user.is_admin = True
    user.is_active = True
    db.session.commit()

    success = True
    results = schema_user.user_schema.dump(user)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')


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
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    user.is_deleted = True
    user.is_active = False

    db.session.commit()

    success = True
    message = 'User successfully deleted'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')


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
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_bio_schema.load(data)

            user = models.User.query.filter_by(
                username=username, is_active=True, is_deleted=False, secret_code=None).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

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

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


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
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_email_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], is_active=True, is_deleted=False).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            email.password_reset_email(user)

            message = 'Check your email for password reset secret code'
            success = True

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


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
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        if not data.get('secret_code'):
            error = {'secret_code': 'This is a required field'}
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            user = models.User.query.filter_by(
                secret_code=data['secret_code'], is_active=True, is_deleted=False).first()
        except Exception as e:
            pass

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        user.secret_code = None
        db.session.commit()

        message = 'Secret code valid'
        success = True

        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


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
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_user.user_password_change_schema.load(data)

            user = models.User.query.filter_by(
                email=clean_data['email'], is_active=True, is_deleted=False).first()

            if not user:
                error = 'User not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            user.password = util.hash_password(clean_data['password'])

            db.session.commit()

            message = 'User password successfully updated, you can now login'
            success = True

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except ValidationError as e:
            error = e.normalized_messages()
    else:
        error = "Json data is required"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/<string:username>/refresh_token', methods=['GET'])
def refresh_token(username):
    error = None
    message = None
    success = False
    results = None

    try:
        user = models.User.query.filter_by(
            username=username, is_active=True, is_deleted=False).first()

        if not user:
            error = 'User not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        new_token = token.generate_token(user)

        schema_user.user_schema.dump

        message = 'Token successfully refreshed'
        success = True

        return jsonify({'token': new_token}), util.http_status_code('SUCCESS')

    except ValidationError as e:
        error = e.normalized_messages()

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@account.route('/test', methods=['GET'])
def test():
    print('HERE.......................')
    print(request.headers['Authorization'].split(' ')[-1], '#######')
    return jsonify({'message': 'WORKING'}), 200
