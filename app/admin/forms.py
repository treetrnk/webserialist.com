from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError

required = "<span class='text-danger'>*</span>"

# Add forms here
class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=75)])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    email = StringField('Email', validators=[Length(max=120), Email()])
    about_me = TextAreaField('About Me', validators=[Length(max=1000)])
    website = StringField('Website', validators=[Length(max=300)])

class GroupEditForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=75)])
    description = TextAreaField('Description', validators=[Length(max=300)])
    style = SelectField('Style')

class GenreEditForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=75)])
    icon = StringField('Icon', validators=[Length(max=150)])
    parent_id = SelectField('Parent Genre', coerce=int)

class FictionEditForm(FlaskForm):
    pass

class SubscriberEditForm(FlaskForm):
    pass


