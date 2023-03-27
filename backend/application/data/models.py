from application.data.database import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    dp_url = db.Column(db.String)
    active = db.Column(db.Boolean(), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    posted_by = db.Column(db.String, nullable = False)
    
class UserFollows(db.Model):
    __tablename__ = "userfollows"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False)
    follows = db.Column(db.Integer, nullable = False)
