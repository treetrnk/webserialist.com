from flask import render_template, redirect, flash, url_for, current_app
from app import db
from app.main import bp
from flask_login import login_required, current_user
from app.main.generic_views import SaveObjView, DeleteObjView
from app.main.forms import FictionEditForm, SubscribeForm
from app.models import Fiction, Subscriber

# Add routes here
@bp.route('/fiction/<int:obj_id>')
@bp.route('/fiction/<int:obj_id>/<string:slug>')
@login_required # DELETE WHEN READY
def fiction(obj_id, slug=''):
    #fiction = Fiction.query.filter_by(id=obj_id, approval=True).first()
    fiction = Fiction.query.filter_by(id=obj_id).first()
    current_app.logger.debug(f'Fiction: {fiction}')

    return render_template('main/fiction.html',
            fiction=fiction,
        )

@bp.route('/top')
@bp.route('/top/<string:source>')
@bp.route('/top/<string:source>/<string:sort>')
@login_required # DELETE WHEN READY
def top_stories(source=None, sort=None):
    fictions = Fiction.query.all()
    return render_template('main/top.html',
                title = 'Top Stories',
                fictions = fictions,
        )

@bp.route('/landing-page')
def landing_page():
    return render_template('index.html')

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return top_stories()
    return landing_page()

class AddFiction(SaveObjView):
    title = "Add Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Add'
    log_msg = 'added a fiction'
    success_msg = 'Fiction added.'
    delete_endpoint = 'main.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        current_app.logger.debug(self.form.__dict__)
        self.form.status.choices = Fiction.STATUS_CHOICES
    
    def post_post(self):
        if self.form.author_claim.data == True:
            self.obj.author_id = current_user.id
        self.obj.updater_id = current_user.id

bp.add_url_rule("/fiction/add", 
        view_func=login_required(AddFiction.as_view('add_fiction')))

class EditFiction(SaveObjView):
    title = "Edit Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Edit'
    log_msg = 'updated a fiction'
    success_msg = 'Fiction updated.'
    delete_endpoint = 'main.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        self.form.status.choices = Fiction.STATUS_CHOICES

bp.add_url_rule("/fiction/edit/<int:obj_id>", 
        view_func=login_required(EditFiction.as_view('edit_fiction')))

class DeleteFiction(DeleteObjView):
    model = Fiction
    log_msg = 'deleted a fiction'
    success_msg = 'Fiction deleted.'
    redirect = {'endpoint': 'main.profile'}

bp.add_url_rule("/fiction/delete", 
        view_func = login_required(DeleteFiction.as_view('delete_fiction')))

class AddSubscriber(SaveObjView):
    title = "Add Subscriber"
    model = Subscriber
    form = SubscribeForm
    action = 'Add'
    log_msg = 'added a subscriber'
    success_msg = 'Subscriber added.'
    delete_endpoint = 'main.delete_subscriber'
    template = 'object-edit.html'
    redirect = {'endpoint': 'main.index'}

bp.add_url_rule("/subscrib", 
        view_func=AddSubscriber.as_view('subscribe'))

class DeleteSubscriber(DeleteObjView):
    model = Subscriber
    log_msg = 'deleted a subscriber'
    success_msg = 'Subscriber deleted.'
    redirect = {'endpoint': 'main.index'}

bp.add_url_rule("/unsubscribe", 
        view_func = login_required(DeleteSubscriber.as_view('unsubscribe')))

