from marshmallow.exceptions import ValidationError
from marshmallow import validates

from app import ma, models


class UserSchema(ma.Schema):
    id = ma.Integer()
    username = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True)
    profile_pic = ma.String()
    bio = ma.String()
    location = ma.String()
    website = ma.Url()
    is_active = ma.Boolean()
    is_admin = ma.Boolean()
    joined_date = ma.DateTime()


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class LoginSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.String(required=True)


login_schema = LoginSchema()


class UserBioSchema(ma.Schema):
    bio = ma.String()
    location = ma.String()
    website = ma.String()


user_bio_schema = UserBioSchema()


class UserEmailSchema(ma.Schema):
    email = ma.Email(required=True)


user_email_schema = UserEmailSchema()


class UserPasswordChangeSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.String(required=True)


user_password_change_schema = UserPasswordChangeSchema()


class PostSchema(ma.Schema):
    class Meta:
        fields = ['id', 'body', 'user_id', 'posted_date', 'liked', 'comments']

    @validates('body')
    def validate_body(self, body):
        if len(body) <= 0:
            raise ValidationError('This field is a required field.')

    @validates('user_id')
    def validate_user_id(self, user_id):
        if type(user_id) != 'int':
            raise ValidationError('Invalid field data type')
        elif not user_id:
            raise ValidationError('This field is a required field')


post_schema = PostSchema()
post_schemas = PostSchema(many=True)


class CommentSchema(ma.Schema):
    id = ma.Integer()
    body = ma.String(required=True)
    post_id = ma.Integer(required=True)
    user_id = ma.Integer(required=True)
    comment_date = ma.DateTime()


comment_schema = CommentSchema()
comment_schemas = CommentSchema(many=True)


class NotificationSchema(ma.Schema):
    id = ma.Integer()
    body = ma.String(required=True)
    user_id = ma.Integer(required=True)
    notification_date = ma.DateTime()


notification_schema = NotificationSchema()
notification_schemas = NotificationSchema(many=True)
