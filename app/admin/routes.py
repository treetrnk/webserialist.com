from flask import render_template, redirect, flash, url_for
from app import db
from app.admin import bp
from flask_login import login_required, current_user
from app.models import Subscriber

# Add routes here
@bp.route('/admin/subscribers')
@login_required
def subscribers():
    if current_user.is_authenticated and current_user.username == 'hueyhare' and current_user.id == 1:
        subscribers = Subscriber.query.all()
        return render_template('admin/subscribers.html',
                subscribers=subscribers,
            )
    return redirect(url_for('main.index')), 404
