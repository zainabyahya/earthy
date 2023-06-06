from email.policy import default
from flask import current_app
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer
from earthy import db,  login_manager
from flask_login import UserMixin
from sqlalchemy import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    members = db.Column(db.Integer)
    password = db.Column(db.String(60), nullable=False)
    score=db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    plastics = db.relationship('Plastic', backref='user', passive_deletes=True)

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
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    
    def __repr__(self):
        return f"User('{self.title}', '{self.date_created}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    
    def __repr__(self):
            return f"User('{self.author}', '{self.date_created}', '{self.text}')"

class Plastic(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    creation_datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    plasticBottle=db.Column(db.Integer, default=0)
    plasticBag=db.Column(db.Integer, default=0)
    plasticWrap=db.Column(db.Integer, default=0)
    yoghurtBox=db.Column(db.Integer, default=0)
    cottonSwab=db.Column(db.Integer, default=0)
    detergentBottle=db.Column(db.Integer, default=0)
    shampooBottle=db.Column(db.Integer, default=0)
    toothbrush=db.Column(db.Integer, default=0)
    toothpaste=db.Column(db.Integer, default=0)
    takeawayBox=db.Column(db.Integer, default=0)
    takeawayWrap=db.Column(db.Integer, default=0)
    straw=db.Column(db.Integer, default=0)
    disposableCutlery=db.Column(db.Integer, default=0)
    plasticPlate=db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    