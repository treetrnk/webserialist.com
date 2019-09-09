from flask import current_app, url_for, session, jsonify, render_template
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime
from sqlalchemy import desc

#tags = db.Table('tags',
#    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
#)

genres = db.Table('genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('story_id', db.Integer, db.ForeignKey('story.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(500))
    about_me = db.Column(db.String(140))
    website = db.Column(db.String(300))
    theme = db.Column(db.String(75), default='light')
    timezone = db.Column(db.String(150))
    ratings = db.relationship('Rating', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User({self.username})>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Fiction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(150))
    synopsis = db.Column(db.String(400), nullable=False)
    cover_img = db.Column(db.String(500))
    banner_img = db.Column(db.String(500))
    genres = db.relationship('Genre', secondary=genres, lazy='subquery', 
            backref=db.backref('fictions', lazy=True))
    words = db.Column(db.Integer, default=0)
    website = db.Column(db.String(300), nullable=False)
    author_placeholder = db.Column(db.String(100)) # For unclaimed fictions
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship("User", foreign_keys=[author_id], backref='fictions')
    status = db.Column(db.String(75), nullable=False)
    frequency = db.Column(db.Float) # releases per month
    approval = db.Column(db.Boolean, default=None)
    approval_date = db.Column(db.DateTime, default=None) # True, False, None
    approver_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Fix. 2 user ids
    approver = db.relationship("User", foreign_keys=[approver_id],
            backref='approved_fictions')
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updater = db.relationship("User", foreign_keys=[updater_id])
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    STATUS_CHOICES = (
            #('unkown', 'Unknown'),
            ('haiatus', 'Haiatus'),
            ('ongoing', 'Ongoing'),
            ('complete', 'Complete'),
        )

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Float, nullable=False)
    subject = db.Column(db.String(150))
    comment = db.Column(db.String(5000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(250))
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    icon = db.Column(db.String(150))
    parent_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    parent = db.relationship('Genre', remote_side=[id], backref='subgenres')
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submitter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    submitter = db.relationship("User", foreign_keys=[submitter_id], backref='submissions')
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id')) # For book covers
    path = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    response = db.Column(db.Boolean)
    comment = db.Column(db.String(1000))
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updater = db.relationship("User", foreign_keys=[updater_id], backref='submission_responses')
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

