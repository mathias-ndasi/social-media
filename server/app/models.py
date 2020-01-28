from app import create_app, db, ma
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.String(60), default='default.png')
    bio = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(100), nullabel=True)
    is_active = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Post', backref='user')

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return f'User({self.username})'


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())
