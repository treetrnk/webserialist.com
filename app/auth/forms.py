from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError
from app.models import User

required = "<span class='text-danger'>*</span>"

class SignupForm(FlaskForm):
    username = StringField(f'Username{required}', validators=[DataRequired(), Length(max=64)])
    email = StringField(f'Email{required}', validators=[Length(max=120)])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    password = PasswordField(f'Password{required}', validators=[DataRequired(), Length(max=128)])
    confirm_password = PasswordField(f'Confirm Password{required}', validators=[DataRequired(), EqualTo('password'), Length(max=128)])

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.', 'danger')
        return True
