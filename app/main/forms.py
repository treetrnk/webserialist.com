from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField, FileField, FloatField,
        FormField, FieldList,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError, URL
from app.models import Genre, Subscriber, Tag

required = "<span class='text-danger'>*</span>"

def all_genres(): 
    return Genre.query.order_by('name').all()

def all_tags(): 
    return Tag.query.order_by('name').all()

class LinkAddForm(FlaskForm):
    fiction_id = HiddenField('fiction id', validators=[DataRequired()])
    url = StringField('URL', validators=[Length(max=500), URL()], render_kw={'placeholder': 'https://'})
    default = BooleanField('Default Link?')

class LinkForm(FlaskForm):
    #id = HiddenField('id', render_kw={'class': 'child-id'})
    url = StringField('URL', validators=[Length(max=500), URL()], render_kw={'placeholder': 'https://'})
    default = BooleanField('Default Link?')

class SubmissionEditForm(FlaskForm):
    pending_cover_img = FileField('Cover Image', validators=[Length(max=500)])
    title = StringField(f'Title{required}', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Subtitle', validators=[Length(max=150)])
    synopsis = TextAreaField(f'Synopsis{required}', validators=[DataRequired(), Length(max=1000)],
            render_kw={'rows': '6'})
    genres = QuerySelectMultipleField(f'Genres{required}', 
            render_kw={'data_type': 'select2'}, 
            description="<small class='text-muted'>Pick up to two genres.</small>", 
            query_factory=all_genres)
    tags = QuerySelectMultipleField('Tags', 
            render_kw={'data_type': 'select2'}, 
            description="<small class='text-muted'>Pick up to ten tags.</small>", 
            query_factory=all_tags)
    links = FieldList(FormField(LinkForm), min_entries=1, max_entries=5, label=f'Links{required}')
    rating = SelectField(f'Rating{required}', validators=[DataRequired()])
    #website = StringField('URL', validators=[DataRequired(), Length(max=300)])
    #author_placeholder = StringField('Author')
    status = SelectField(f'Status{required}')
    words = IntegerField(f'Current Word Count{required}', render_kw={'placeholder': '###'})
    frequency = FloatField(f'Releases per Month{required}', render_kw={'placeholder': 'Decimals are allowed'})
    author_claim = BooleanField(f'Are you the Author?{required}', description="<small class='text-muted'>By checking this box you agree that you hold the copyright to this work and have the rights to upload it here.</small>")

    def validate_genres(self, genres):
        if len(self.genres.data) > 2:
            raise ValidationError('You can only pick up to two genres.')

    def validate_tags(self, tags):
        if len(self.tags.data) > 2:
            raise ValidationError('You can only pick up to ten tags.')

class FictionEditForm(FlaskForm):
    obj_id = HiddenField()
    cover_img = FileField('Cover Image')
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Subtitle', validators=[Length(max=150)])
    synopsis = TextAreaField('Synopsis', validators=[DataRequired(), Length(max=1000)],
            render_kw={'rows': '6'})
    genres = QuerySelectMultipleField('Genres', render_kw={'data_type': 'select2'}, query_factory=all_genres)
    links = FieldList(FormField(LinkForm), max_entries=5, label=f'Links{required}')
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

class FictionSearchForm(FlaskForm):
    keywords = StringField('Search', validators=[Length(max=200)])
    genres = SelectMultipleField('Genres', render_kw={'data_type': 'select2'})
    tags = SelectMultipleField('Tags', render_kw={'data_type': 'select2'})
    sort = SelectField('Sort By')

class DeleteObjForm(FlaskForm):
    obj_id = HiddenField('Object id', validators=[DataRequired()])
