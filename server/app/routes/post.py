from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql.expression import delete

from app import db, models
from app.auth import decorators
from app.schemas import schema_post, schema_user
from app.utils import util

post_api = Blueprint('post_api', __name__, url_prefix='/post')


@post_api.route('/create', methods=['POST'])
@decorators.token_required
def post_create():
    error = {'body': None}
    message = None
    success = False
    results = None

    if request.is_json:
        try:
            data = request.get_json()

            if not data:
                error['body'] = 'Json data is missen'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error['body'] = 'Json data is missen'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            clean_data = schema_post.post_validate_schema.load(data)

        except ValidationError as e:
            error = e.normalized_messages()
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            user = models.User.query.filter_by(
                id=clean_data['user_id']).first()

            if not user:
                error['body'] = 'Invalid user_id parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            new_post = models.Post(body=clean_data['body'], created_by=user.id)

            db.session.add(new_post)
            db.session.commit()

            success = True
            message = "New post created successfully!!!"
            results = schema_post.post_schema.dump(new_post)
            results['liked_by'] = []
            results['comments'] = []

            for liked in new_post.liked_post:
                results['liked_by'].append(liked.user.username)

            for comment in new_post.comments:
                data = {'body': comment.body, 'commented_by': comment.commented_by,
                        'comment_date': comment.comment_date}
                results['comments'].append(data)

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('CREATED')

        except Exception as e:
            error['body'] = 'Invalid user_id parsed'

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@post_api.route('/<int:post_id>/update', methods=['PUT'])
@decorators.token_required
def post_update(post_id):
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
            clean_data = schema_post.post_validate_schema.load(data)

        except ValidationError as e:
            error = e.normalized_messages()
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            user = models.User.query.filter_by(
                id=clean_data['user_id']).first()

            if not user:
                error = 'Invalid user_id parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Invalid user_id parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            post = models.Post.query.filter_by(
                id=post_id, created_by=user.id).first()

            if not post:
                error = 'Post not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            post.body = clean_data['body']

            db.session.commit()
            success = True
            message = "Post updated successfully!!!"
            results = schema_post.post_schema.dump(post)
            results['liked_by'] = []
            results['comments'] = []

            for liked in post.liked_post:
                results['liked_by'].append(liked.user.username)

            for comment in post.comments:
                data = {'body': comment.body, 'commented_by': comment.commented_by,
                        'comment_date': comment.comment_date}
                results['comments'].append(data)

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except Exception as e:
            error = 'Post not found'

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


# TODO: successfully delete a post found in a many-to-many relationship
@post_api.route('/<int:post_id>/delete', methods=['DELETE'])
@decorators.token_required
def post_delete(post_id):
    error = None
    message = None
    success = False
    results = None

    try:
        post = models.Post.query.filter_by(
            id=post_id).first()
        print(post, '#################')

        if not post:
            error = 'Post not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        print('1 #################')

        liked_post = models.LikedPost.query.filter_by(post_id=post.id).first()
        # print(liked_post, '########')
        # if liked_post:
        db.session.delete(liked_post)
        db.session.commit()

        print('2 #################')
        db.session.delete(post)
        db.session.commit()

        success = True
        message = "Post successfully deleted"

        print('3 #################')

        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

    except Exception as e:
        print(e, '#################')
        error = 'Post not found...'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@post_api.route('/<int:post_id>/<string:username>', methods=['GET'])
@decorators.token_required
def get_single_user_post(post_id, username):
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
            user = models.User.query.filter_by(
                id=data['user_id'], username=username).first()

            if not user:
                error = 'Invalid user_id or username parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Invalid user_id or username parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            post = models.Post.query.filter_by(
                id=post_id, created_by=user.id).first()

            if not post:
                error = 'Post not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            # try:
            #     user = models.User.query.filter_by(id=post.created_by).first()

            success = True
            results = schema_post.post_schema.dump(post)
            results['liked_by'] = []
            results['comments'] = []

            for liked in post.liked_post:
                results['liked_by'].append(liked.user.username)

            for comment in post.comments:
                data = {'body': comment.body, 'commented_by': comment.commented_by,
                        'comment_date': comment.comment_date}
                results['comments'].append(data)

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except Exception as e:
            error = 'Post not found'

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@post_api.route('/<string:username>', methods=['GET'])
@decorators.token_required
def get_all_user_post(username):
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
            user = models.User.query.filter_by(
                id=data['user_id'], username=username).first()

            if not user:
                error = 'Invalid user_id or username parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Invalid user_id parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            posts = models.Post.query.filter_by(created_by=user.id).all()

            if not posts:
                error = 'No post found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            success = True

            results = []
            for post in posts:
                data = schema_post.post_schema.dump(post)
                data['liked_by'] = []
                data['comments'] = []

                for liked in post.liked_post:
                    data['liked_by'].append(liked.user.username)

                for comment in post.comments:
                    comment_data = {'body': comment.body, 'commented_by': comment.commented_by,
                                    'comment_date': comment.comment_date}
                    data['comments'].append(comment_data)

                results.append(data)

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except Exception as e:
            error = 'No post found'

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@post_api.route('/<int:post_id>', methods=['GET'])
@decorators.token_required
def get_single_post(post_id):
    error = None
    message = None
    success = False
    results = None

    try:
        post = models.Post.query.filter_by(
            id=post_id).first()

        if not post:
            error = 'Post not found'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        success = True
        results = schema_post.post_schema.dump(post)
        results['liked_by'] = []
        results['comments'] = []

        for liked in post.liked_post:
            results['liked_by'].append(liked.user.username)

        for comment in post.comments:
            data = {'body': comment.body, 'commented_by': comment.commented_by,
                    'comment_date': comment.comment_date}
            results['comments'].append(data)

        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

    except Exception as e:
        error = 'Post not found'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')


@post_api.route('', methods=['GET'])
@decorators.token_required
def get_all_post():
    error = None
    message = None
    success = False
    results = None

    posts = models.Post.query.order_by(db.desc('id')).all()

    if not posts:
        error = 'No post found'
        return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

    success = True

    results = []
    for post in posts:
        created_user = models.User.query.filter_by(id=post.created_by).first()
        data = schema_post.post_schema.dump(post)
        data['created_by'] = schema_user.user_schema.dump(created_user)
        data['liked_by'] = []
        data['comments'] = []

        for liked in post.liked_post:
            data['liked_by'].append(liked.user.username)

        for comment in post.comments:
            comment_data = {'body': comment.body, 'commented_by': comment.commented_by,
                            'comment_date': comment.comment_date}
            data['comments'].append(comment_data)

        results.append(data)

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')


@post_api.route('/like/<int:post_id>', methods=['PUT'])
@decorators.token_required
def like_post(post_id):
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
            user = models.User.query.filter_by(
                id=data['user_id']).first()

            if not user:
                error = 'Invalid user_id parsed'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        except Exception as e:
            error = 'Invalid user_id parsed'
            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

        try:
            post = models.Post.query.filter_by(
                id=post_id).first()

            if not post:
                error = 'Post not found'
                return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')

            if user in post.liked_by:
                post.liked = False
                post.no_likes -= 1
                post.liked_by.remove(user)
                message = "Post successfully unliked"
            else:
                post.liked = True
                post.no_likes += 1
                post.liked_by.append(user)
                message = "Post successfully liked"

            db.session.commit()
            success = True

            results = schema_post.post_schema.dump(post)
            results['liked_by'] = []
            results['comments'] = []

            for liked in post.liked_post:
                results['liked_by'].append(liked.user.username)

            for comment in post.comments:
                data = {'body': comment.body, 'commented_by': comment.commented_by,
                        'comment_date': comment.comment_date}
                results['comments'].append(data)

            return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('SUCCESS')

        except Exception as e:
            error = 'Post not found'

    else:
        error = 'Only Json data is required'

    return jsonify({'success': success, 'data': results, 'message': message, 'error': error}), util.http_status_code('BAD_REQUEST')
