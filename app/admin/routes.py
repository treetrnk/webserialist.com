from flask import render_template, redirect, flash, url_for
from app import db
from app.admin import bp
from flask_login import login_required, current_user
from app.auth.authenticators import group_required
from app.admin.forms import (
        FictionEditForm, SubscriberEditForm, UserEditForm,
        GenreEditForm, GroupEditForm, TagEditForm, SubmissionEditForm,
    )
from app.main.generic_views import SaveObjView, DeleteObjView
from app.models import Subscriber, User, Fiction, Genre, Group, Tag, Submission

##########
## USER ##
##########
@bp.route('/admin/users')
@group_required('admin')
def users():
    if current_user.is_authenticated and current_user.username == 'hueyhare' and current_user.id == 1:
        users = User.query.all()
        return render_template('admin/users.html',
                users=users,
                tab='users',
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
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.users'}
    context = {'tab': 'users'}

    def extra(self):
        self.form.theme.choices = User.THEME_CHOICES
    
bp.add_url_rule("/admin/users/add", 
        view_func=group_required('admin')(AddUser.as_view('add_user')))

class EditUser(SaveObjView):
    title = "Edit User"
    model = User
    form = UserEditForm
    action = 'Edit'
    log_msg = 'updated a user'
    success_msg = 'User updated.'
    delete_endpoint = 'admin.delete_user'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.users'}
    context = {'tab': 'users'}

    def extra(self):
        self.form.theme.choices = User.THEME_CHOICES
    
bp.add_url_rule("/admin/users/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditUser.as_view('edit_user')))

class DeleteUser(DeleteObjView):
    model = User
    log_msg = 'deleted a user'
    success_msg = 'User deleted.'
    redirect = {'endpoint': 'admin.users'}

bp.add_url_rule("/admin/users/delete", 
        view_func = group_required('admin')(DeleteUser.as_view('delete_user')))

###########
## GROUP ##
###########
@bp.route('/admin/groups')
@group_required('admin')
def groups():
    groups = Group.query.all()
    return render_template('admin/groups.html',
            groups=groups,
            tab='groups',
        )

class AddGroup(SaveObjView):
    title = "Add Group"
    model = Group
    form = GroupEditForm
    action = 'Add'
    log_msg = 'added a group'
    success_msg = 'Group added.'
    delete_endpoint = 'admin.delete_group'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.groups'}
    context = {'tab': 'groups'}

    def extra(self):
        self.form.style.choices = Group.STYLE_CHOICES

bp.add_url_rule("/admin/groups/add", 
        view_func=group_required('admin')(AddGroup.as_view('add_group')))

class EditGroup(SaveObjView):
    title = "Edit Group"
    model = Group
    form = GroupEditForm
    action = 'Edit'
    log_msg = 'updated a group'
    success_msg = 'Group updated.'
    delete_endpoint = 'admin.delete_group'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.groups'}
    context = {'tab': 'groups'}

    def extra(self):
        self.form.style.choices = Group.STYLE_CHOICES

bp.add_url_rule("/admin/groups/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditGroup.as_view('edit_group')))

class DeleteGroup(DeleteObjView):
    model = Group
    log_msg = 'deleted a group'
    success_msg = 'Group deleted.'
    redirect = {'endpoint': 'admin.groups'}

bp.add_url_rule("/admin/groups/delete", 
        view_func = group_required('admin')(DeleteGroup.as_view('delete_group')))

################
## SUBSCRIBER ##
################
@bp.route('/admin/subscribers')
@group_required('admin')
def subscribers():
    subscribers = User.query.all()
    return render_template('admin/subscribers.html',
            subscribers=subscribers,
            tab='subscribers',
        )

class AddSubscriber(SaveObjView):
    title = "Add Subscriber"
    model = Subscriber
    form = SubscriberEditForm
    action = 'Add'
    log_msg = 'added a subscriber'
    success_msg = 'Subscriber added.'
    delete_endpoint = 'admin.delete_subscriber'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.subscribers'}
    context = {'tab': 'subscribers'}

bp.add_url_rule("/admin/subscribers/add", 
        view_func=group_required('admin')(AddSubscriber.as_view('add_subscriber')))

class EditSubscriber(SaveObjView):
    title = "Edit Subscriber"
    model = Subscriber
    form = SubscriberEditForm
    action = 'Edit'
    log_msg = 'updated a subscriber'
    success_msg = 'Subscriber updated.'
    delete_endpoint = 'admin.delete_subscriber'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.subscribers'}
    context = {'tab': 'subscribers'}

bp.add_url_rule("/admin/subscribers/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditSubscriber.as_view('edit_subscriber')))

class DeleteSubscriber(DeleteObjView):
    model = Subscriber
    log_msg = 'deleted a subscriber'
    success_msg = 'Subscriber deleted.'
    redirect = {'endpoint': 'admin.subscribers'}

bp.add_url_rule("/admin/subscribers/delete", 
        view_func = group_required('admin')(DeleteSubscriber.as_view('delete_subscriber')))

#############
## FICTION ##
#############
@bp.route('/admin/fictions')
@group_required('admin')
def fictions():
    fictions = Fiction.query.all()
    return render_template('admin/fictions.html',
            fictions=fictions,
            tab='fictions',
        )

class AddFiction(SaveObjView):
    title = "Add Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Add'
    log_msg = 'added a fiction'
    success_msg = 'Fiction added.'
    delete_endpoint = 'admin.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.fictions'}
    context = {'tab': 'fictions'}

bp.add_url_rule("/admin/fictions/add", 
        view_func=group_required('admin')(AddFiction.as_view('add_fiction')))

class EditFiction(SaveObjView):
    title = "Edit Fiction"
    model = Fiction
    form = FictionEditForm
    action = 'Edit'
    log_msg = 'updated a fiction'
    success_msg = 'Fiction updated.'
    delete_endpoint = 'admin.delete_fiction'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.fictions'}
    context = {'tab': 'fictions'}

bp.add_url_rule("/admin/fictions/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditFiction.as_view('edit_fiction')))

class DeleteFiction(DeleteObjView):
    model = Fiction
    log_msg = 'deleted a fiction'
    success_msg = 'Fiction deleted.'
    redirect = {'endpoint': 'admin.fictions'}

bp.add_url_rule("/admin/fictions/delete", 
        view_func = group_required('admin')(DeleteFiction.as_view('delete_fiction')))

################
## SUBMISSION ##
################
@bp.route('/admin/submissions')
@group_required('admin')
def submissions(status='pending'):
    if status == 'approved':
        submissions = Submission.query.filter_by(approval=True).all()
    elif status == 'approved':
        submissions = Submission.query.filter_by(approval=False).all()
    else:
        submissions = Submission.query.filter_by(approval=None).all()
    return render_template('admin/submissions.html',
            submissions=submissions,
            tab='submissions',
            status=status,
        )

@bp.route('/admin/submissions/approved')
@group_required('admin')
def submissions_approved():
    return submissions(status='approved')

@bp.route('/admin/submissions/rejected')
@group_required('admin')
def submissions_rejected():
    return submissions(status='rejected')

class AddSubmission(SaveObjView):
    title = "Add Submission"
    model = Submission
    form = SubmissionEditForm
    action = 'Add'
    log_msg = 'added a submission'
    success_msg = 'Submission added.'
    delete_endpoint = 'admin.delete_submission'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.submissions'}
    context = {'tab': 'submissions'}

bp.add_url_rule("/admin/submissions/add", 
        view_func=group_required('admin')(AddSubmission.as_view('add_submission')))

class EditSubmission(SaveObjView):
    title = "Edit Submission"
    model = Submission
    form = SubmissionEditForm
    action = 'Edit'
    log_msg = 'updated a submission'
    success_msg = 'Submission updated.'
    delete_endpoint = 'admin.delete_submission'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.submissions'}
    context = {'tab': 'submissions'}

bp.add_url_rule("/admin/submissions/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditSubmission.as_view('edit_submission')))

class DeleteSubmission(DeleteObjView):
    model = Submission
    log_msg = 'deleted a submission'
    success_msg = 'Submission deleted.'
    redirect = {'endpoint': 'admin.submissions'}

bp.add_url_rule("/admin/submissions/delete", 
        view_func = group_required('admin')(DeleteSubmission.as_view('delete_submission')))

###########
## GENRE ##
###########
@bp.route('/admin/gernes')
@group_required('admin')
def genres():
    genres = Genre.query.all()
    return render_template('admin/genres.html',
            genres=genres,
            tab='genres',
        )

class AddGenre(SaveObjView):
    title = "Add Genre"
    model = Genre
    form = GenreEditForm
    action = 'Add'
    log_msg = 'added a genre'
    success_msg = 'Genre added.'
    delete_endpoint = 'admin.delete_genre'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.genres'}
    context = {'tab': 'fictions'}

    def extra(self):
        self.form.parent_id.choices = [(0,'')] + [(g.id,g) for g in Genre.query.all()]

    def pre_post(self):
        if self.form.parent_id.data == 0:
            self.form.parent_id.data = None

bp.add_url_rule("/admin/genres/add", 
        view_func=group_required('admin')(AddGenre.as_view('add_genre')))

class EditGenre(SaveObjView):
    title = "Edit Genre"
    model = Genre
    form = GenreEditForm
    action = 'Edit'
    log_msg = 'updated a genre'
    success_msg = 'Genre updated.'
    delete_endpoint = 'admin.delete_genre'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.genres'}
    context = {'tab': 'fictions'}

    def extra(self):
        self.form.parent_id.choices = [(0,'')] + [(g.id,g) for g in Genre.query.all()]

    def pre_post(self):
        if self.form.parent_id.data == 0:
            self.form.parent_id.data = None

bp.add_url_rule("/admin/genres/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditGenre.as_view('edit_genre')))

class DeleteGenre(DeleteObjView):
    model = Genre
    log_msg = 'deleted a genre'
    success_msg = 'Genre deleted.'
    redirect = {'endpoint': 'admin.genres'}

bp.add_url_rule("/admin/genres/delete", 
        view_func = group_required('admin')(DeleteGenre.as_view('delete_genre')))

#########
## TAG ##
#########
@bp.route('/admin/tags')
@group_required('admin')
def tags():
    tags = Tag.query.all()
    return render_template('admin/tags.html',
            tags=tags,
            tab='tags',
        )

class AddTag(SaveObjView):
    title = "Add Tag"
    model = Tag
    form = TagEditForm
    action = 'Add'
    log_msg = 'added a tag'
    success_msg = 'Tag added.'
    delete_endpoint = 'admin.delete_tag'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.tags'}
    context = {'tab': 'fictions'}

bp.add_url_rule("/admin/tags/add", 
        view_func=group_required('admin')(AddTag.as_view('add_tag')))

class EditTag(SaveObjView):
    title = "Edit Tag"
    model = Tag
    form = TagEditForm
    action = 'Edit'
    log_msg = 'updated a tag'
    success_msg = 'Tag updated.'
    delete_endpoint = 'admin.delete_tag'
    template = 'object-edit.html'
    redirect = {'endpoint': 'admin.tags'}
    context = {'tab': 'fictions'}

bp.add_url_rule("/admin/tags/edit/<int:obj_id>", 
        view_func=group_required('admin')(EditTag.as_view('edit_tag')))

class DeleteTag(DeleteObjView):
    model = Tag
    log_msg = 'deleted a tag'
    success_msg = 'Tag deleted.'
    redirect = {'endpoint': 'admin.tags'}

bp.add_url_rule("/admin/tag/delete", 
        view_func = group_required('admin')(DeleteTag.as_view('delete_tag')))

