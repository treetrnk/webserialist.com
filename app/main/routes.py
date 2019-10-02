from flask import render_template, redirect, flash, url_for
from app import db
from app.main import bp
from flask_login import login_required, current_user
from app.main.generic_views import SaveObjView, DeleteObjView
from app.main.forms import FictionEditForm
from app.models import Fiction

# Add routes here
@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/top')
@bp.route('/top/<string:source>')
@bp.route('/top/<string:source>/<string:sort>')
def top_stories(source=None, sort=None):
    fictions = Fiction.query.all()
    return render_template('main/top.html',
                title = 'Top Stories',
                fictions = fictions,
        )

class AddFiction(SaveObjView):
    title = "Add Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Add'
    log_msg = 'added a fiction'
    success_msg = 'Fiction added.'
    delete_endpoint = 'main.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'main.profile'}

bp.add_url_rule("/fiction/add", 
        view_func=AddFiction.as_view('add_fiction'))

class EditFiction(SaveObjView):
    title = "Edit Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Edit'
    log_msg = 'updated a fiction'
    success_msg = 'Fiction updated.'
    delete_endpoint = 'main.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'main.profile'}

bp.add_url_rule("/fiction/edit/<int:obj_id>", 
        view_func=EditFiction.as_view('edit_fiction'))

class DeleteFiction(DeleteObjView):
    model = Fiction
    log_msg = 'deleted a fiction'
    success_msg = 'Fiction deleted.'
    redirect = {'endpoint': 'main.profile'}

bp.add_url_rule("/fiction/delete", 
        view_func = DeleteFiction.as_view('delete_fiction'))

