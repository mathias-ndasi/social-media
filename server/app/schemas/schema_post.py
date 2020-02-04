from marshmallow.exceptions import ValidationError
from marshmallow import validates

from app import ma, models


class PostSchema(ma.Schema):
    id = ma.Integer()
    body = ma.String(required=True)
    created_by = ma.Integer()
    no_likes = ma.Integer()
    no_comments = ma.Integer()
    posted_date = ma.DateTime()
    liked = ma.Boolean()

    @validates('body')
    def validate_body(self, body):
        if len(body) <= 0:
            raise ValidationError("This field can't be empty.")
        elif len(body) > 255:
            raise ValidationError('max character of 255 characters exceeded.')


post_schema = PostSchema()
post_schemas = PostSchema(many=True)


class PostValidateSchema(ma.Schema):
    id = ma.Integer()
    user_id = ma.Integer(required=True)
    body = ma.String(required=True)

    @validates('body')
    def validate_body(self, body):
        if len(body) <= 0:
            raise ValidationError("This field can't be empty.")
        elif len(body) > 255:
            raise ValidationError('max character of 255 characters exceeded.')


post_validate_schema = PostValidateSchema()


class CommentSchema(ma.Schema):
    id = ma.Integer()
    body = ma.String(required=True)
    post_id = ma.Integer()
    commented_by = ma.Integer(required=True)
    comment_date = ma.DateTime()


comment_schema = CommentSchema()
comment_schemas = CommentSchema(many=True)


class NotificationSchema(ma.Schema):
    id = ma.Integer()
    body = ma.String(required=True)
    created_by = ma.Integer(required=True)
    target_user = ma.Integer(required=True)
    notification_date = ma.DateTime()

    @validates('body')
    def validate_body(self, body):
        if len(body) <= 0:
            raise ValidationError("This field can't be empty.")
        elif len(body) > 255:
            raise ValidationError('max character of 255 characters exceeded.')


notification_schema = NotificationSchema()
notification_schemas = NotificationSchema(many=True)
