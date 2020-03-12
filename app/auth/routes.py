from flask import render_template, redirect, flash, url_for, request, abort, current_app
from app import db
from app.auth import bp
from flask_login import login_required, current_user, login_user, logout_user
from app.auth.forms import SignupForm, LoginForm, ProfileEditForm
from app.models import User
from app.main.generic_views import SaveObjView, DeleteObjView

# Add routes here
@bp.route('/signup', methods=['GET', 'POST'])
def signup(tab='Sign Up'):
    flash('Sign ups are currently closed.', 'warning')
    signup_form = SignupForm()
    login_form = LoginForm()
    return render_template('auth/login.html',
            title = tab,
            signup_form = signup_form,
            login_form = login_form,
            tab = tab,
        )

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return signup(tab='Login')

@bp.route('/process-signup', methods=['POST'])
def process_signup():
    """
    form = SignupForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome to Web Serialist.com!', 'success')
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.login'))
    """
    current_app.logger.info(f"New Sign Up attempt: {request.form['first_name']} - {request.form['last_name']} - {request.form['email']}")
    flash('We are not accepting new users at the moment. Thank you for your interest!', 'warning')
    return redirect(url_for('main.index'))


@bp.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('Invalid username!', 'danger')
            return redirect(url_for('auth.login'))
        if not user.check_password(form.password.data):
            flash('Invalid password!', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('You are now logged in.', 'success')
        #next = request.args.get('next')
        #if not is_safe_url(next):
        #    return abort(400)
        return redirect(url_for('main.top_stories'))
    return redirect(url_for('auth.login')) 

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('main.top_stories'))

@bp.route("/profile")
@bp.route("/profile/<string:username>")
@login_required # DELETE WHEN READY
def profile(username=None):
    if username:
        user = User.query.filter_by(username=username).first()
    else: 
        if not current_user.is_authenticated:
            return '404 Error - Page not found', 404
        user = User.query.filter_by(id=current_user.id).first()
    return render_template('/auth/profile.html',
            user = user,
            title = f"{user.display_name()}'s Profile",
        )

class EditProfile(SaveObjView):
    title = "User Settings"
    model = User
    form = ProfileEditForm
    action = 'Edit'
    log_msg = 'updated their profile'
    success_msg = 'Profile updated.'
    delete_endpoint = 'auth.delete_user'
    template = 'object-edit.html'
    redirect = {'endpoint': 'auth.profile'}

    def extra(self):
        self.form.theme.choices = [('light','Light'), ('dark','Dark')]
        self.form.timezone.choices = [('est','EST')]

bp.add_url_rule("/profile/edit/<int:obj_id>", 
        view_func=login_required(EditProfile.as_view('edit_profile')))

class DeleteUser(DeleteObjView):
    model = User
    log_msg = 'deleted a user'
    success_msg = 'User deleted.'
    redirect = {'endpoint': 'main.index'}

bp.add_url_rule("/profile/delete", 
        view_func = login_required(DeleteUser.as_view('delete_user')))
