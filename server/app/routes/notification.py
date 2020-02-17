from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from app import models, db
from app.schemas import schema_post
from app.auth import decorators
from app.utils import util


notification_api = Blueprint(
    'notification_api', __name__, url_prefix='/notification')


@notification_api.route('/<string:username>', methods=['POST'])
@decorators.token_required
def create_notification(username):
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
            clean_data = schema_post.notification_schema.load(data)

        except ValidationError as e:
            error = e.normalized_messages()
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            target_user = models.User.query.filter_by(
                id=clean_data['target_user']).first()

            if not target_user:
                error = 'Invalid target user_id parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Invalid target user_id parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            notification_user = models.User.query.filter_by(
                id=clean_data['created_by'], username=username).first()

            if not notification_user:
                error = 'Invalid created_by user_id or username parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Invalid created_by user_id or username parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        new_notification = models.Notification(
            body=clean_data['body'], created_by=notification_user.id, target_user=target_user.id)

        target_user.notifications.append(new_notification)

        db.session.add(new_notification)
        db.session.commit()

        success = True
        message = "Notification created successfully!!!"

        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('CREATED')

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@notification_api.route('/<int:notification_id>', methods=['DELETE'])
@decorators.token_required
def delete_notification(notification_id):
    error = None
    message = None
    success = False
    results = None

    try:
        notification = models.Notification.query.filter_by(
            id=notification_id).first()

        if not notification:
            error = 'Invalid notification_id parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    except Exception as e:
        error = 'Invalid notification_id parsed'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    try:
        notification_user = models.User.query.filter_by(
            id=notification.target_user).first()

        if not notification_user:
            error = 'Notification not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    except Exception as e:
        error = 'Notification not found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    target_user.notifications.remove(notification)

    db.session.delete(notification)
    db.session.commit()

    success = True
    message = "Notification deleted successfully!!!"

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')
