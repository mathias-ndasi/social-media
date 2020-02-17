import os
import random
import secrets
from string import ascii_letters, digits

from flask import request
from PIL import Image

from app import bcrypt
from app.config import Config
from app.models import User


def http_status_code(status):
    return {
        # success
        'SUCCESS': 200,
        'CREATED': 201,
        'NO_CONTENT': 204,
        # client
        'BAD_REQUEST': 400,
        'UNAUTHORIZED': 401,
        'FORBIDDEN': 403,
        'NOT_FOUND': 404,
        # server
        'INTERNAL_SERVER_ERROR': 500,
    }.get(status)


# Get secret code
def generate_secret_code(current_user, *args, **kwargs):
    token_1 = secrets.token_hex(2)
    token_2 = ''.join(str(x) for x in random.choices(ascii_letters, k=2))
    token_3 = ''.join(str(x) for x in random.choices(digits, k=2))
    code = token_1 + token_2 + token_3

    for user in User.query.all():
        if code == user.secret_code:
            generate_secret_code(current_user)

    return code


# Generate user password hash
def hash_password(password, *args, **kwargs):
    # returns hashed password
    pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return pwd_hash


# Verify user password hash
def verify_password(user, password, *args, **kwargs):
    # returns true or false
    hash_pwd = user.password
    if bcrypt.check_password_hash(hash_pwd, password):
        return True
    else:
        return False


# Resizing and saving picture
def save_picture(form_picture, user, *args, **kwargs):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    file_ext = form_picture.filename.split('.')[-1].lower()
    random_hex = secrets.token_hex(5)

    if file_ext in ALLOWED_EXTENSIONS:
        picture_file_name = f"{random_hex}.{file_ext}"
        picture_path = Config.BASE_DIR + '/app/static/profile_pics/' + \
            user.username + '/profile/' + picture_file_name

        try:
            os.makedirs(
                f"{Config.BASE_DIR + '/app/static/profile_pics'}/{user.username}/profile")
        except FileExistsError as e:
            pass

        pic_server_path = f'{Config.BASE_URL}/static/profile_pics/{user.username}/profile/{picture_file_name}'

        # if len(os.listdir(os.path.dirname(picture_path))) > 0:
        #     for file in os.listdir(os.path.dirname(picture_path)):
        #         os.remove(
        #             f"{Config.BASE_DIR + '/app/static/profile_pics'}/{user.username}/profile/{file}")

        output_size = (125, 125)
        image = Image.open(form_picture)
        image.thumbnail(output_size)
        image.save(picture_path)

        return pic_server_path
    else:
        return None
