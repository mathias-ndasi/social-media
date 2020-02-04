from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from app import models, db
from app.schemas import schema_post
from app.auth import decorators


comment_api = Blueprint('comment_api', __name__, url_prefix='/comment')


@comment_api.route('/<int:post_id>', methods=['PUT'])
@decorators.token_required
def create_comment(post_id):
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
            clean_data = schema_post.comment_schema.load(data)

        except ValidationError as e:
            error = e.normalized_messages()
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            user = models.User.query.filter_by(
                id=clean_data['commented_by']).first()

            if not user:
                error = 'Invalid user_id parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        except Exception as e:
            error = 'Invalid user_id parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        try:
            post = models.Post.query.filter_by(
                id=post_id).first()

            if not post:
                error = 'Post not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

            new_comment = models.Comment(
                body=clean_data['body'], post_id=post_id, commented_by=clean_data['commented_by'])

            post.comments.append(new_comment)
            post.no_comments += 1

            db.session.add(new_comment)
            db.session.commit()
            success = True
            message = "Post comment successfully!!!"

            results = schema_post.post_schema.dump(post)
            results['liked_by'] = []
            results['comments'] = []

            for liked in post.liked_post:
                results['liked_by'].append(liked.user.username)

            for com in post.comments:
                data = {'body': com.body, 'user_id': com.commented_by,
                        'comment_date': com.comment_date}
                results['comments'].append(data)

        except Exception as e:
            error = 'Post not found'

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})


@comment_api.route('/<int:post_id>', methods=['GET'])
@decorators.token_required
def get_all_comments(post_id):
    error = None
    message = None
    success = False
    results = None

    try:
        post = models.Post.query.filter_by(
            id=post_id).first()

        if not post:
            error = 'Invalid post_id'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error})

        success = True
        message = "comments loaded"

        results = schema_post.post_schema.dump(post)
        results['liked_by'] = []
        results['comments'] = []

        for liked in post.liked_post:
            results['liked_by'].append(liked.user.username)

        for com in post.comments:
            data = {'body': com.body, 'user_id': com.commented_by,
                    'comment_date': com.comment_date}
            results['comments'].append(data)

    except Exception as e:
        error = 'Invalid post_id'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error})
