from flask import render_template, redirect, flash, url_for
from app import db
from app.forum import bp
from flask_login import login_required, current_user

# Add routes here
