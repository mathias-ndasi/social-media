import datetime
from flask import jsonify, request
from flask_mail import Message

from app import mail, db
from app.models import User
from app.utils.util import generate_secret_code
from app.config import Config


# account creation email
def account_comfirmation_email(user, *args, **kwargs):
    secret_code = generate_secret_code(user)
    msg = Message(subject='Tiki Account Confirmation',
                  sender=Config.MAIL_USERNAME, recipients=[user.email])
    msg.body = f"""
        Below is your Tiki account confirmation  code:

        {secret_code}
        
        If you did not make this message then simply ignore this email and no changes will be made.    
        """

    mail.send(msg)

    user.secret_code = secret_code
    db.session.add(user)
    db.session.commit()


# password reset email
def password_reset_email(user, *args, **kwargs):
    secret_code = generate_secret_code(user)
    msg = Message(subject='Tiki Password Reset',
                  sender=Config.MAIL_USERNAME, recipients=[user.email])
    msg.body = f"""
    Below is your secret code for a successfull password reset:
    
    {secret_code}
    
    If you did not make this message then simply ignore this email and no changes will be made.
    """
    mail.send(msg)

    user.secret_code = secret_code
    db.session.add(user)
    db.session.commit()
