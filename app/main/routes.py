from flask import render_template, redirect, flash, url_for
from app import db
from app.main import bp
from flask_login import login_required, current_user
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
