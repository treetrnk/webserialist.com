import re
from markdown import markdown
from flask import current_app, url_for, session, jsonify, render_template
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime
from sqlalchemy import desc, func
from sqlalchemy.orm import backref
from urllib.parse import urlparse
#from app.main.functions import process_markdown

fiction_genres = db.Table('fiction_genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('fiction_id', db.Integer, db.ForeignKey('fiction.id'), primary_key=True)
)
submission_genres = db.Table('proposal_genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('submission_id', db.Integer, db.ForeignKey('submission.id'), primary_key=True)
)
fiction_tags = db.Table('fiction_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('fiction_id', db.Integer, db.ForeignKey('fiction.id'), primary_key=True)
)
submission_tags = db.Table('proposal_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('submission_id', db.Integer, db.ForeignKey('submission.id'), primary_key=True)
)
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
    genres = db.relationship('Genre', secondary=fiction_genres, lazy='subquery', 
            backref=db.backref('fictions', lazy=True))
    tags = db.relationship('Tag', secondary=fiction_tags, lazy='subquery', 
            backref=db.backref('fictions', lazy=True))
    rating = db.Column(db.String(20))
    words = db.Column(db.Integer, default=0)
    website = db.Column(db.String(300))
    author_placeholder = db.Column(db.String(100)) # For unclaimed fictions
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author = db.relationship("User", foreign_keys=[author_id], backref='fictions')
    status = db.Column(db.String(75), nullable=False)
    frequency = db.Column(db.Float) # releases per month
    rating_average = db.Column(db.Float)
    total_views = db.Column(db.Integer)
    weekly_views = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    weekly_votes = db.Column(db.Integer)
    total_votes = db.Column(db.Integer)
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
            ('ongoing', 'Ongoing'),
            ('complete', 'Complete'),
            ('haiatus', 'Haiatus'),
            ('abandoned', 'Abandoned'),
        )

    RATING_CHOICES = (
            ('G', 'G - Acceptable for all audiences'),
            ('PG', 'PG - May contain some simple violence'),
            ('PG-13', 'PG-13 - Acceptable for ages 13 and up'),
            ('R', 'R - Contains graphic violence and/or sexual content'),
            ('X', 'X - The focus is on sexual content'),
        )

    SEARCH_SORT_CHOICES = [
            ('rating,desc', 'Rating (High ⭢ Low)'),
            ('rating,asc', 'Rating (Low ⭢ High)'),
            #('views,desc', 'Views (High ⭢ Low)'),
            #('views,asc', 'Views (Low ⭢ High)'),
            ('votes,desc', 'Votes (High ⭢ Low)'),
            ('votes,asc', 'Votes (Low ⭢ High)'),
            ('random', 'Random Order'),
        ]

    def update_rating(self):
        ratings = Rating.query.filter_by(fiction_id = self.id).all()
        total = 0
        if ratings:
            for rating in ratings:
                total += rating.stars
            self.rating_average = total / len(ratings)

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

    """
    def view_count(self, limit=None):
        if limit == 'unique':
            views = View.query.filter_by(fiction_id=self.id).with_entities(View.session_id).distinct().all()
        else: 
            views = self.views
        return len(views)
    """

    def snippet(self, length=150):
        output = self.html()
        if len(self.html()) > length:
            output = self.html()[0:length] + '...'
        else:
            output = self.text() + '...'
        output = remove_breaks(output)
        return output

    def average_rating(self, return_type=None):
        if return_type == 'stars':
            output = ''
            star_num = 0.5
            for i in range(0,5):
                if self.rating_average and self.rating_average >= star_num:
                    output += "<i class='fas fa-star text-yellow'></i>"
                else:
                    output += "<i class='fas fa-star text-muted'></i>"
                star_num += 1.0
            return output
        elif return_type == 'float':
            return self.rating_average if self.rating_average else 0
        return self.rating_average if self.rating_average else 'No ratings yet'

    def simple_frequency(self):
        return str(self.frequency).rstrip('0').rstrip('.')
        
    def __repr__(self):
        return f'Fiction({self.id}, {self.title})'

    def __str__(self):
        return self.title

################
## SUBMISSION #######################################################################
################
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    fiction = db.relationship("Fiction", backref='submissions')
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(150))
    synopsis = db.Column(db.String(1000), nullable=False)
    cover_img = db.Column(db.String(500))
    banner_img = db.Column(db.String(500))
    genres = db.relationship('Genre', secondary=submission_genres, lazy='subquery', 
            backref=db.backref('submissions', lazy=True))
    tags = db.relationship('Tag', secondary=submission_tags, lazy='subquery', 
            backref=db.backref('submissions', lazy=True))
    rating = db.Column(db.String(20))
    words = db.Column(db.Integer, default=0)
    website = db.Column(db.String(300))
    author_placeholder = db.Column(db.String(100)) 
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author = db.relationship("User", foreign_keys=[author_id], backref='author_submissions')
    status = db.Column(db.String(75), nullable=False)
    frequency = db.Column(db.Float) # releases per month
    approval = db.Column(db.Boolean, default=None)
    approval_date = db.Column(db.DateTime, default=None) # True, False, None
    approver_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Fix. 2 user ids
    approver = db.relationship("User", foreign_keys=[approver_id],
            backref='approved_submissions')
    submitter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    submitter = db.relationship("User", foreign_keys=[submitter_id], backref='submissions')
    updater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updater = db.relationship("User", foreign_keys=[updater_id])
    updated = db.Column(db.DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow, nullable=False)

    def text_approval(self):
        if self.approval == True:
            return 'Approved'
        if self.approval == False:
            return 'Rejected'
        return 'Pending'


    def html(self):
        output = ''
        if self.synopsis:
            output = process_markdown(self.synopsis)
            output = remove_complicated_html(output)
            output = remove_links(output)
        return output

    def snippet(self, length=150):
        output = self.html()
        if len(self.html()) > length:
            output = self.html()[0:length] + '...'
        else:
            output = self.text() + '...'
        output = remove_breaks(output)
        return output

    def __repr__(self):
        return f'Submissions({self.id}, {self.title})'

    def __str__(self):
        return self.title

##########
## LINK ############################################################
##########
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    fiction = db.relationship('Fiction', backref=backref('links', order_by=desc('default')))
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    submission = db.relationship('Submission', backref=backref('links', order_by=desc('default')))
    url = db.Column(db.String(500), nullable=False)
    default = db.Column(db.Boolean)

    def set_default(self):
        links = Link.query.filter_by(fiction_id=self.fiction_id).all()
        for link in links:
            link.default = False
        self.default = True

    def domain(self):
        domain = urlparse(self.url).netloc.replace('www.','')
        return domain[0].upper() + domain[1:]

    def __str__(self):
        return f"{self.url[0:20]}..."

    def __repr__(self):
        return f"<Link({self.id}, {self.url[:20]}...)>"

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

#############
## COMMENT #####################################################################
#############
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='comments', lazy=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    submission = db.relationship('Submission', backref=backref('comments', order_by='Comment.created.desc()'), lazy=True)
    text = db.Column(db.String(5000), nullable=False, default=' ')
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    hidden = db.Column(db.Boolean, default=False)

    def html_text(self):
        return markdown(self.text)

    def created_local(self):
        utc_created = pytz.utc.localize(self.created)
        return utc_created.astimezone(tz.tzlocal())

    def notify(self, edited_user, subject="New Comment", url='/', item=''):
        if edited_user.id == self.user.id:
            recipients = [m.email for m in edited_user.get_managers()]        
        else:
            recipients = [edited_user.email]
            for manager in edited_user.get_managers():
                if self.user.id != manager.id:
                    recipients += [manager.email]
        recipients = [e for e in recipients if e]
        if len(recipients) == 0:
            print("Could not send email(s). No recipients!")
            return False
        base_url = current_app.config['BASE_URL']
        subject = subject + f' by {self.user.display_name_short()}' if self.user else subject
        text_body = f"EBS Portal Notification\n\nA new comment by {self.user.display_name_short()} was made on {item}.\n\nView it here: {base_url+url}"
        send_email(
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                subject=subject,
                recipients=recipients,
                text_body=text_body,
                html_body=render_template('email/comment.html',
                        url=base_url + url,
                        user=self.user,
                        comment=self,
                        item=item,
                        debug=current_app.config.get("DEBUG"),
                    )
            )
        return recipients

    def __repr__(self):
            return f"Comment({self.id}, '{self.user}', '{self.submission_id}', '{self.text}')"


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

