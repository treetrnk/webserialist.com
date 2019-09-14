from flask import render_template, redirect, flash, url_for, request, abort
from app import db
from app.auth import bp
from flask_login import login_required, current_user, login_user, logout_user
from app.auth.forms import SignupForm, LoginForm
from app.models import User

# Add routes here
@bp.route('/signup', methods=['GET', 'POST'])
def signup(tab='Sign Up'):
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
    form = SignupForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome to Web Serialist.com!', 'success')
        return redirect(url_for('main.top_stories'))
    return render_template('auth/signup.html',
            title = 'Sign Up',
            form = form,
        )


@bp.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('Invalid username!', 'danger')
            return redirect(request.url)
        if not user.check_password(form.password.data):
            flash('Invalid password!', 'danger')
            return redirect(request.url)
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
