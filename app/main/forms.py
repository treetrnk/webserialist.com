from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField, FileField, FloatField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError
from app.models import Genre, Subscriber

required = "<span class='text-danger'>*</span>"

def all_genres(): 
    return Genre.query.order_by('name').all()

# Add forms here
class FictionEditForm(FlaskForm):
    cover_img = FileField('Cover Image')
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Subtitle', validators=[Length(max=150)])
    synopsis = TextAreaField('Synopsis', validators=[DataRequired(), Length(max=1000)],
            render_kw={'rows': '6'})
    genres = QuerySelectMultipleField('Genres', render_kw={'data_type': 'select2'}, query_factory=all_genres)
    website = StringField('URL', validators=[DataRequired(), Length(max=300)])
    author_claim = BooleanField('Are you the Author?')
    author_placeholder = StringField('Author')
    status = SelectField('Status')
    words = IntegerField('Current Word Count')
    frequency = FloatField('Releases per Month')

class SubscribeForm(FlaskForm):
    email = StringField(f'Email Address{required}', validators=[Email(), DataRequired()])
    email_confirm = StringField(f'Confirm Email{required}', validators=[Email(), EqualTo('email'), DataRequired()])
    first_name = StringField('First Name', validators=[Length(max=75)])
    last_name = StringField('Last Name', validators=[Length(max=75)])
    comment = TextAreaField('Comments', render_kw={'placeholder': 'How did you hear about WS? What features are you most excited about?\nOther comments?'}, validators=[Length(max=75)])

    def validate_email(self, email):
        sub = Subscriber.query.filter_by(email=self.email.data).first()
        if sub:
            raise ValidationError('You are already subscribed!', 'Error')
        return True

class DeleteObjForm(FlaskForm):
    obj_id = HiddenField('Object id', validators=[DataRequired()])
