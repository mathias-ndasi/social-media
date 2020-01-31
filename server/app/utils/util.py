import os
import random
import secrets
from string import ascii_letters, digits

from flask import request
from PIL import Image

from app import bcrypt
from app.config import Config
from app.models import User


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
    random_hex = secrets.token_hex(8)
    file_ext = form_picture.filename.split('.')[-1].lower()

    if file_ext in ALLOWED_EXTENSIONS:
        picture_file_name = 'profile.' + file_ext
        picture_path = Config.BASE_DIR + '/app/static/profile_pics/' + \
            user.username + '/profile/' + picture_file_name

        try:
            os.makedirs(
                f"{Config.BASE_DIR + '/app/static/profile_pics'}/{user.username}/profile")
        except FileExistsError as e:
            pass

        if len(os.listdir(os.path.dirname(picture_path))) > 0:
            for file in os.listdir(os.path.dirname(picture_path)):
                os.remove(
                    f"{Config.BASE_DIR + '/app/static/profile_pics'}/{user.username}/profile/{file}")

        output_size = (125, 125)
        image = Image.open(form_picture)
        image.thumbnail(output_size)
        image.save(picture_path)

        return picture_path
    else:
        return None
