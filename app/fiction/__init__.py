from flask import Blueprint

bp = Blueprint('fiction', __name__)

from app.fiction import routes
