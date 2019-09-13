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
class AddFictionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Subtitle', validators=[Length(max=150)])
    synopsis = StringField('Synopsis', validators=[DataRequired(), Length(max=400)])
    cover_img = FileField('Cover Image')
    generes = QuerySelectMultipleField('Genres')
    website = StringField('URL', validators=[DataRequired(), Length(max=300)])
    author_claim = BooleanField('Are you the Author?')
    author_placeholder = StringField('Author', validators=[DataRequried()])
    status = SelectField('Status')
    frequency = FloatField('Releases per Month')
