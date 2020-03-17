from flask import render_template, redirect, flash, url_for
from app import db
from app.admin import bp
from flask_login import login_required, current_user
from app.auth.authenticators import group_required
from app.admin.forms import (
        FictionEditForm, SubscriberEditForm, UserEditForm,
        GenreEditForm,
    )
from app.main.generic_views import SaveObjView, DeleteObjView
from app.models import Subscriber, User, Fiction, Genre

# Add routes here
@bp.route('/admin/users')
@group_required('admin')
def users():
    if current_user.is_authenticated and current_user.username == 'hueyhare' and current_user.id == 1:
        users = User.query.all()
        return render_template('admin/users.html',
                users=users,
            )
    return redirect(url_for('main.index')), 404

class AddUser(SaveObjView):
    title = "Add User"
    model = User
    form = UserEditForm
    action = 'Add'
    log_msg = 'added a user'
    success_msg = 'User added.'
    delete_endpoint = 'admin.delete_user'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.users'}

bp.add_url_rule("/admin/user/add", 
        view_func=group_required('admin')(AddUser.as_view('add_user')))

class EditUser(SaveObjView):
    title = "Edit User"
    model = User
    form = UserEditForm
    action = 'Edit'
    log_msg = 'updated a user'
    success_msg = 'User updated.'
    delete_endpoint = 'admin.delete_user'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.users'}

bp.add_url_rule("/admin/user/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditUser.as_view('edit_user')))

class DeleteUser(DeleteObjView):
    model = User
    log_msg = 'deleted a user'
    success_msg = 'User deleted.'
    redirect = {'endpoint': 'admin.users'}

bp.add_url_rule("/admin/user/delete", 
        view_func = group_required('admin')(DeleteUser.as_view('delete_user')))

@bp.route('/admin/subscribers')
@login_required
def subscribers():
    if current_user.is_authenticated and current_user.username == 'hueyhare' and current_user.id == 1:
        subscribers = User.query.all()
        return render_template('admin/subscribers.html',
                subscribers=subscribers,
            )
    return redirect(url_for('main.index')), 404

class AddSubscriber(SaveObjView):
    title = "Add Subscriber"
    model = Subscriber
    form = SubscriberEditForm
    action = 'Add'
    log_msg = 'added a subscriber'
    success_msg = 'Subscriber added.'
    delete_endpoint = 'admin.delete_subscriber'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.subscribers'}

bp.add_url_rule("/admin/subscriber/add", 
        view_func=login_required(AddSubscriber.as_view('add_subscriber')))

class EditSubscriber(SaveObjView):
    title = "Edit Subscriber"
    model = Subscriber
    form = SubscriberEditForm
    action = 'Edit'
    log_msg = 'updated a subscriber'
    success_msg = 'Subscriber updated.'
    delete_endpoint = 'admin.delete_subscriber'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.subscribers'}

bp.add_url_rule("/admin/subscriber/edit/<int:obj_id>", 
        view_func=login_required(EditSubscriber.as_view('edit_subscriber')))

class DeleteSubscriber(DeleteObjView):
    model = Subscriber
    log_msg = 'deleted a subscriber'
    success_msg = 'Subscriber deleted.'
    redirect = {'endpoint': 'admin.subscribers'}

bp.add_url_rule("/admin/subscriber/delete", 
        view_func = login_required(DeleteSubscriber.as_view('delete_subscriber')))

@bp.route('/admin/fiction')
@group_required('admin')
def fictions():
    fictions = Fiction.query.all()
    return render_template('admin/fictions.html',
            fictions=fictions,
        )

@bp.route('/admin/fiction/submissions')
@group_required('admin')
def submissions():
    fictions = Fiction.query.all()
    return render_template('admin/fictions.html',
            fictions=fictions,
        )

class AddFiction(SaveObjView):
    title = "Add Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Add'
    log_msg = 'added a fiction'
    success_msg = 'Fiction added.'
    delete_endpoint = 'admin.delete_fiction'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.fictions'}

bp.add_url_rule("/admin/fiction/add", 
        view_func=login_required(AddFiction.as_view('add_fiction')))

class EditFiction(SaveObjView):
    title = "Edit Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Edit'
    log_msg = 'updated a fiction'
    success_msg = 'Fiction updated.'
    delete_endpoint = 'admin.delete_fiction'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.fictions'}

bp.add_url_rule("/admin/fiction/edit/<int:obj_id>", 
        view_func=login_required(EditFiction.as_view('edit_fiction')))

class DeleteFiction(DeleteObjView):
    model = Fiction
    log_msg = 'deleted a fiction'
    success_msg = 'Fiction deleted.'
    redirect = {'endpoint': 'admin.fictions'}

bp.add_url_rule("/admin/fiction/delete", 
        view_func = login_required(DeleteFiction.as_view('delete_fiction')))

@bp.route('/admin/gerne')
@group_required('admin')
def genres():
    genres = Genre.query.all()
    return render_template('admin/genres.html',
            genres=genres,
        )

class AddGenre(SaveObjView):
    title = "Add Genre"
    model = Genre
    form = GenreEditForm
    action = 'Add'
    log_msg = 'added a genre'
    success_msg = 'Genre added.'
    delete_endpoint = 'admin.delete_genre'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.genres'}

bp.add_url_rule("/admin/genre/add", 
        view_func=login_required(AddGenre.as_view('add_genre')))

class EditGenre(SaveObjView):
    title = "Edit Genre"
    model = Genre
    form = GenreEditForm
    action = 'Edit'
    log_msg = 'updated a genre'
    success_msg = 'Genre updated.'
    delete_endpoint = 'admin.delete_genre'
    template = 'admin/object-edit.html'
    redirect = {'endpoint': 'admin.genres'}

bp.add_url_rule("/admin/genre/edit/<int:obj_id>", 
        view_func=login_required(EditGenre.as_view('edit_genre')))

class DeleteGenre(DeleteObjView):
    model = Genre
    log_msg = 'deleted a genre'
    success_msg = 'Genre deleted.'
    redirect = {'endpoint': 'admin.genres'}

bp.add_url_rule("/admin/genre/delete", 
        view_func = login_required(DeleteGenre.as_view('delete_genre')))

