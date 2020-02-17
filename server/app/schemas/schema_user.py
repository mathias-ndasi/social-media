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

    @validates('password')
    def validate_password(self, password):
        if len(password) < 4:
            raise ValidationError('Password is too short')


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
