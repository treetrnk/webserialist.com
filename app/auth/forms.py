from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField, FileField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

required = "<span class='text-danger'>*</span>"

class SignupForm(FlaskForm):
    username = StringField(f'Username{required}', validators=[DataRequired(), Length(max=64)])
    email = StringField(f'Email{required}', validators=[Length(max=120)])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    password = PasswordField(f'Password{required}', 
            validators=[DataRequired(), Length(max=128)],
            description="<small class='text-muted'>Password must contain at least one uppercase character, one lowercase character, and a number.</small>")
    confirm_password = PasswordField(f'Confirm Password{required}', validators=[DataRequired(), EqualTo('password'), Length(max=128)])

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.', 'danger')
        return True

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('Email address already in use.', 'danger')
        return True

    def validate_password(self, password):
        if self.password.data:
            password = self.password.data
            success = True
            specials = ['~','!','@','#','$','%','^','&','*','(',')','-','_','=','+']
            if not any(char.isupper() for char in password):
                success = False
            if not any(char.islower() for char in password):
                success = False
            if not any(char.isdigit() for char in password):
                success = False
            if not success:
                raise ValidationError('New password must include at least one uppercase character, one lowercase character, and a number.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        user = User.query.filter_by(username = self.username.data).first()
        if not user:
            raise ValidationError("The username {self.username.data} doesn't exist. Please sign up for a new account if you don't already have one.")

    def validate_password(self, password):
        user = User.query.filter_by(username = self.username.data).first()
        if not user.check_password(self.password.data):
            raise ValidationError('Incorrect password for this account.')

class ProfileEditForm(FlaskForm):
    #username = StringField(f'Username{required}', validators=[DataRequired(), Length(max=64)])
    #email = StringField(f'Email{required}', validators=[Length(max=120), Email()])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    #avatar = FileField('Avatar', validators=[Length(max=500)])
    website = StringField('Website', validators=[Length(max=300)])
    about_me = TextAreaField('About Me', validators=[Length(max=1000)])
    #theme = SelectField('Theme', validators=[Length(max=75)])
    #timezone = SelectField('Timezone', validators=[Length(max=150)])

class UserSettingsForm(FlaskForm):
    #username = StringField(f'Username{required}', validators=[DataRequired(), Length(max=64)])
    email = StringField(f'Email{required}', validators=[Length(max=120), Email()])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    theme = SelectField('Theme', validators=[Length(max=75)])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', 
            validators=[Length(min=8,max=128), Optional()],
            description="<small class='text-muted'>Password must contain at least one uppercase character, one lowercase character, and a number.</small>")
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('new_password')])
    #timezone = SelectField('Timezone', validators=[Length(max=150)])

    def validate_current_password(self, current_password):
        if self.current_password.data:
            if not current_user.check_password(self.current_password.data):
                raise ValidationError('Incorrect password')

    def validate_new_password(self, new_password):
        if self.new_password.data:
            password = self.new_password.data
            success = True
            specials = ['~','!','@','#','$','%','^','&','*','(',')','-','_','=','+']
            if not any(char.isupper() for char in password):
                success = False
            if not any(char.islower() for char in password):
                success = False
            if not any(char.isdigit() for char in password):
                success = False
            if not success:
                raise ValidationError('New password must include at least one uppercase character, one lowercase character, and a number.')
