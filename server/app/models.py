from flask import request
from app import create_app, db
from datetime import datetime
from app.config import Config


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(255))
    profile_pic = db.Column(
        db.String(), default=Config.BASE_URL+'/static/default.png')
    bio = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Post', secondary='liked_post', backref=db.backref(
        "liked_post", cascade="all, delete-orphan"), single_parent=True)
    secret_code = db.Column(db.String(8), nullable=True)
    notifications = db.relationship(
        'Notification', backref=db.backref("user", cascade="all, delete-orphan"), single_parent=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, username, email, password, *args, **kwargs):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User({self.username[:30]+'...'})"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    no_likes = db.Column(db.Integer, default=0)
    no_comments = db.Column(db.Integer, default=0)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow())
    liked = db.Column(db.Boolean, default=False)
    liked_by = db.relationship('User', secondary='liked_post', backref=db.backref(
        "liked_post", cascade="all, delete-orphan"), single_parent=True)
    comments = db.relationship('Comment', backref='post')

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, body, created_by, *args, **kwargs):
        self.body = body
        self.created_by = created_by

    def __repr__(self):
        return f"Post({self.body[:10]+'...'}|{self.posted_date}|{self.created_by})"


class LikedPost(db.Model):
    __tablename__ = 'liked_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.relationship(User, backref=db.backref(
        "liked_post", cascade="all, delete-orphan"), single_parent=True)
    post = db.relationship(Post, backref=db.backref(
        "liked_post", cascade="all, delete-orphan"), single_parent=True)


# liked_post = db.Table('liked_post', db.Model.metadata,
#                       db.Column('user_id', db.Integer, db.ForeignKey(
#                           'user.id', ondelete='cascade'), primary_key=True),
#                       db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='cascade'), primary_key=True))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    commented_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_date = db.Column(db.DateTime, default=datetime.utcnow())

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, body, post_id, commented_by, *args, **kwargs):
        self.body = body
        self.post_id = post_id
        self.commented_by = commented_by

    def __repr__(self):
        return f"Comment({self.body[:10]+'...'}|{self.comment_date}|{self.commented_by})"


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    created_by = db.Column(db.Integer)
    target_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification_date = db.Column(db.DateTime, default=datetime.utcnow())

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, body, created_by, target_user, *args, **kwargs):
        self.body = body
        self.created_by = created_by
        self.target_user = target_user

    def __repr__(self):
        return f"Notification({self.body[:10]+'...'}|{self.created_by})"
