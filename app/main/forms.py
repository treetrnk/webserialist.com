from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField, FileField, FloatField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError

required = "<span class='text-danger'>*</span>"

# Add forms here
class FictionEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Subtitle', validators=[Length(max=150)])
    synopsis = TextAreaField('Synopsis', validators=[DataRequired(), Length(max=400)],
            render_kw={'rows': '6'})
    cover_img = FileField('Cover Image')
    generes = QuerySelectMultipleField('Genres', render_kw={'data_type': 'select2'})
    website = StringField('URL', validators=[DataRequired(), Length(max=300)])
    author_claim = BooleanField('Are you the Author?')
    author_placeholder = StringField('Author', validators=[DataRequired()])
    status = SelectField('Status')
    frequency = FloatField('Releases per Month')
    
class DeleteObjForm(FlaskForm):
    obj_id = HiddenField('Object id', validators=[DataRequired()])
