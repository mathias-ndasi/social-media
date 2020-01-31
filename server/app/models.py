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
        db.String(), default=Config.BASE_DIR+'/app/static/default.png')
    bio = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Post', backref='user')
    secret_code = db.Column(db.String(8), nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User({self.username[:30]+'...'})"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow())
    liked = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='post')

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"Post({self.body[:10]+'...'}|{self.posted_date}|{self.user_id})"


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_date = db.Column(db.DateTime, default=datetime.utcnow())

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, comment, user_id):
        self.comment = comment
        self.user_id = user_id

    def __repr__(self):
        return f"Comment({self.body[:10]+'...'}|{self.comment_date}|{self.user_id})"


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification_date = db.Column(db.DateTime, default=datetime.utcnow())

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, body, user_id):
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return f"Notification({self.body[:10]+'...'}|{self.user_id})"
