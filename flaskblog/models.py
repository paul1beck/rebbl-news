from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    coachname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    role = db.relationship('UserRole', backref='users', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    videos = db.relationship('Video', backref='author', lazy=True)
    comments = db.relationship('PostComment', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"'{self.coachname}', '{self.email}'"


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(60), nullable=False, default='User')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.role}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    shortdesc = db.Column(db.String(250), nullable=True)
    # image_file = db.Column(db.String(20), nullable=True, default='default.png') #For future Cover Image Integration
    sidebar = db.Column(db.Boolean, default=True)
    published = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(20), nullable=True)
    slug = db.Column(db.String(100), nullable=False)
    comments = db.relationship('PostComment', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    video = db.Column(db.Text, nullable=False)
    videotype = db.Column(db.String(20), nullable=True)
    shortdesc = db.Column(db.String(250), nullable=True)
    published = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(20), nullable=True)
    recap = db.Column(db.Boolean, default=False)
    division = db.Column(db.String(20), nullable=True)
    week = db.Column(db.String(20), nullable=True)
    slug = db.Column(db.String(100), nullable=False)
    comments = db.relationship('VideoComment', backref='video', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Video('{self.title}', '{self.date_posted}')"


class VideoComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"
