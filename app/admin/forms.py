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
    pass

class GenreEditForm(FlaskForm):
    pass

class FictionEditForm(FlaskForm):
    pass

class SubscriberEditForm(FlaskForm):
    pass


