from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, 
        BooleanField, SelectMultipleField, SubmitField, FormField,
        PasswordField, HiddenField, FileField, FieldList,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError, URL
from app.models import Group, Fiction, Genre, Tag

required = "<span class='text-danger'>*</span>"

def all_groups():
    return Group.query.order_by('name').all()

def all_genres():
    return Genre.query.order_by('name').all()

def all_tags():
    return Tag.query.order_by('name').all()

# Add forms here
class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=75)])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    email = StringField('Email', validators=[Length(max=120), Email()])
    avatar = FileField('Avatar')
    about_me = TextAreaField('About Me', validators=[Length(max=1000)])
    website = StringField('Website', validators=[Length(max=300)])
    groups = QuerySelectMultipleField('Groups', query_factory=all_groups, render_kw={'data_type': 'select2'}) 
    theme = SelectField('Theme')
    #timezone = SelectField('Timezone')
    password_reset = PasswordField('New Password', validators=[Length(max=30)])
    password_confirm = PasswordField('Confirm Password', validators=[Length(max=30), EqualTo('password_reset')])

class GroupEditForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=75)])
    description = TextAreaField('Description', validators=[Length(max=300)])
    style = SelectField('Style')

class GenreEditForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=75)])
    icon = StringField('Icon', validators=[Length(max=150)])
    parent_id = SelectField('Parent Genre', coerce=int)

class TagEditForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=50)])

class LinkAddForm(FlaskForm):
    fiction_id = HiddenField('fiction id', validators=[DataRequired()])
    url = StringField('URL', validators=[Length(max=500), URL()], render_kw={'placeholder': 'https://'})
    default = BooleanField('Default Link?')

class LinkForm(FlaskForm):
    #id = HiddenField('id', render_kw={'class': 'child-id'})
    url = StringField('URL', validators=[Length(max=500), URL()], render_kw={'placeholder': 'https://'})
    default = BooleanField('Default Link?')

class FictionEditForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=150),DataRequired()])
    subtitle = StringField('Subtitle', validators=[Length(max=150)])
    synopsis = TextAreaField('Synopsis', validators=[Length(max=1000), DataRequired()])
    #cover_img = FileField('Cover Image')
    genres = QuerySelectMultipleField('Genres', query_factory=all_genres, validators=[Length(max=2)], render_kw={'data_type': 'select2'})
    tags = QuerySelectMultipleField('Tags', query_factory=all_tags, render_kw={'data_type': 'select2'})
    links = FieldList(FormField(LinkForm), min_entries=1, max_entries=5, label=f'Links{required}')
    rating = SelectField(f'Rating{required}', validators=[DataRequired()])
    words = IntegerField('Word Count')
    website = StringField('Website', validators=[Length(max=300)])
    author_placeholder = StringField('Author Placeholder', validators=[Length(max=100)])
    author_id = SelectField('Author', coerce=int, render_kw={'data_type': 'select2'})
    status = SelectField('Status')

class SubmissionEditForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Length(max=5000)])
    approve = SubmitField('Approve')

class SubscriberEditForm(FlaskForm):
    pass


