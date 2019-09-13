from flask import render_template, redirect, flash, url_for, request
from app import db
from app.auth import bp
from flask_login import login_required, current_user
from app.auth.forms import SignupForm
from app.models import User

# Add routes here
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
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
