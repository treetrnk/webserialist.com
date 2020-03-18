import re
from markdown import markdown
from flask import current_app, url_for, session, jsonify, render_template
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime
from sqlalchemy import desc, func
from urllib.parse import urlparse
#from app.main.functions import process_markdown

#tags = db.Table('tags',
#    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
#)
groups = db.Table('groups',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_complicated_html(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<\/?(h[1-6]|img).*?>')
    return re.sub(clean, '', text)

def remove_breaks(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<\/?(br|p).*?>')
    return re.sub(clean, '', text)

def remove_links(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<\/?a.*?>')
    return re.sub(clean, '', text)

def process_markdown(text):
    text = remove_html_tags(text)
    return markdown(text)

genres = db.Table('genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('fiction_id', db.Integer, db.ForeignKey('fiction.id'), primary_key=True)
)

##########
## USER #######################################################################
##########
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    groups = db.relationship('Group', secondary=groups, lazy='subquery',
            backref=db.backref('users', lazy=True))
    active = db.Column(db.Boolean, default=True, nullable=False)
    avatar = db.Column(db.String(500))
    about_me = db.Column(db.String(1000))
    website = db.Column(db.String(300))
    theme = db.Column(db.String(75), default='light')
    timezone = db.Column(db.String(150))
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    THEME_CHOICES = [
            ('light', 'Light'),
            ('dark', 'Dark'),
        ]

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def in_group(self, group_names):
        group_names = group_names.split(',')
        my_group_names = [g.name for g in self.groups]
        if 'webdev' in my_group_names:
            return True
        for group_name in group_names:
            if group_name in my_group_names:
                return True
        return False

    def html(self):
        output = ''
        if self.about_me:
            output =  process_markdown(self.about_me)
            output = remove_links(output)
            output = remove_complicated_html(output)
        return output

    def website_domain(self):
        return urlparse(self.website).netloc

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User({self.username})>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

###########
## GROUP #######################################################################
###########
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), unique=True)
    description = db.Column(db.String(300), nullable=True)
    style = db.Column(db.String(75), default='info')
    #restricted = db.Column(db.Boolean(), default=False)
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'))#, onupdate=current_user.id, default=current_user.id)
    updater = db.relationship('User', lazy=True)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    STYLE_CHOICES = [
            ('info', 'Info (Gray-blue)'),
            ('primary', 'Primary (Bright blue)'),
            ('secondary', 'Secondary (Gray)'),
            ('success', 'Success (Green)'),
            ('warning', 'Warning (Orange)'),
            ('danger', 'Danger (Red)'),
            ('light', 'Light (White)'),
            ('dark', 'Dark (Black)'),
            ('RED', 'Red'),
            ('ORG', 'Orange'),
            ('YLW', 'Yellow'),
            ('GRN', 'Green'),
            ('BLU', 'Blue'),
            ('PUR', 'Purple'),
            ('PNK', 'Pink'),
            ('GRY', 'Gray'),
            ('WHT', 'White'),
            ('BLK', 'Black'),
        ]

    def all_permissions(self):
        return [p for p in self.permissions]

    def __repr__(self):
        return f'Group({self.id}, {self.name})'

    def __str__(self):
        return self.name

#############
## FICTION #######################################################################
#############
class Fiction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(150))
    synopsis = db.Column(db.String(1000), nullable=False)
    cover_img = db.Column(db.String(500))
    banner_img = db.Column(db.String(500))
    genres = db.relationship('Genre', secondary=genres, lazy='subquery', 
            backref=db.backref('fictions', lazy=True))
    words = db.Column(db.Integer, default=0)
    website = db.Column(db.String(300), nullable=False)
    author_placeholder = db.Column(db.String(100)) # For unclaimed fictions
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
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
            ('unkown', 'Unknown'),
            ('haiatus', 'Haiatus'),
            ('ongoing', 'Ongoing'),
            ('complete', 'Complete'),
            ('abandoned', 'Abandoned'),
        )

    def html(self):
        output = ''
        if self.synopsis:
            output = process_markdown(self.synopsis)
            output = remove_complicated_html(output)
            output = remove_links(output)
        return output

    def website_domain(self):
        return urlparse(self.website).netloc

    def text(self):
        pattern = re.compile(r'<.*?>')
        return pattern.sub('', self.html())

    def view_count(self, limit=None):
        if limit == 'unique':
            views = View.query.filter_by(fiction_id=self.id).with_entities(View.session_id).distinct().all()
        else: 
            views = self.views
        return len(views)

    def snippet(self, length=150):
        output = self.html()
        if len(self.html()) > length:
            output = self.html()[0:length] + '...'
        else:
            output = self.text() + '...'
        output = remove_breaks(output)
        return output

    def average_rating(self, return_type=None):
        ratings = Rating.query.filter_by(fiction_id=self.id).with_entities(func.avg(Rating.stars).label('average')).all()
        if ratings[0][0]:
            current_app.logger.debug(int(ratings[0][0]))
        not_available = None
        if return_type == 'text':
            not_available = 'No ratings yet'
        elif return_type == 'float':
            not_available = 0
        return ratings[0][0] if ratings[0][0] else not_available

    def simple_frequency(self):
        return str(self.frequency).rstrip('0').rstrip('.')
        
    def __repr__(self):
        return f'Fiction({self.id}, {self.title})'

    def __str__(self):
        return self.title

############
## RATING #######################################################################
############
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Float, nullable=False)
    subject = db.Column(db.String(150))
    comment = db.Column(db.String(5000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='ratings', lazy=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), nullable=False)
    fiction = db.relationship('Fiction', backref='ratings', lazy=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Rating({self.id}, {self.stars})'

    def __str__(self):
        return self.subject

##########
## VOTE #######################################################################
##########
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='votes', lazy=True)
    ip_address = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(250))
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), nullable=False)
    fiction = db.relationship('Fiction', backref='votes', lazy=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Vote({self.id}, {user.id})'

    def __str__(self):
        return self.id

##########
## VIEW #######################################################################
##########
class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), nullable=False)
    fiction = db.relationship('Fiction', backref='views', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='views', lazy=True)
    #ip = db.Column(db.String(15))
    session_id = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 

    def __repr__(self):
        return f'View({self.id})'

    def __str__(self):
        return self.id

###########
## GENRE #######################################################################
###########
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    icon = db.Column(db.String(150))
    parent_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    parent = db.relationship('Genre', remote_side=[id], backref='subgenres')
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Genre({self.id}, {self.name})'

    def __str__(self):
        return self.name

#########
## TAG #######################################################################
#########
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Tag({self.id}, {self.name})'

    def __str__(self):
        return self.name

################
## SUBMISSION #######################################################################
################
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

    def __repr__(self):
        return f'Submission({self.id})'

    def __str__(self):
        return self.id

################
## SUBSCRIBER #######################################################################
################
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True) 
    first_name = db.Column(db.String(75), nullable=True)
    last_name = db.Column(db.String(75), nullable=True)
    comment = db.Column(db.String(1000))
    sub_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'Subscriber({self.id}, {self.email})'

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

