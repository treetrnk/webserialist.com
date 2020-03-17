from flask import redirect, flash, url_for, g, current_app, request
from flask_login import current_user
from functools import wraps

def group_required(groups, fail_redirect=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user is None:
                flash(f'You must login to access that page!', 'danger')
                return redirect(url_for('auth.login'))
            if not current_user.active:
                flash(f'Your account has been deactivated. Please speak with your supervisor to regain access.', 'danger')
                current_app.logger.warning(f"Authentication Failure: {current_user.username}'s account is inactive.")
                return redirect(url_for('auth.logout'))
            if not current_user.in_group(groups):
                message = ("Permissions Warning:\n"    
                        f"    url = {request.url}\n"
                        f"    current_user = {current_user.username},\n"
                        f"    groups required = {groups}\n"
                        f"    {current_user.username} is not in the correct"
                        " group to access to this page.\n")
                current_app.logger.warning(message)
                flash(f'You are not authorized to visit that page!<br /><small>Groups allowed: <b>{groups}</b></small>', 'danger')
                return redirect(url_for('auth.login')) if not fail_redirect else fail_redirect
            return func(*args, **kwargs)
        return wrapper
    return decorator

"""
def user_permission_required(permissions, fail_redirect=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from app.models import User
            username = kwargs['username'] if 'username' in kwargs else args[0]
            user = User.query.filter_by(username=username).first()
            if not user.has_permission(permissions):
                message = ("User Permissions Warning:\n"    
                        f"    url = {request.url}\n"
                        f"    current_user = {current_user.username},\n"
                        f"    accessed_user = {user.username},\n"
                        f"    permissions required = {permissions}\n"
                        f"    {user.username} does not have the correct"
                        " permissions to grant access to this page.\n")
                current_app.logger.warning(message)
                flash(f'{user.display_name_short()} must have the <b>{permissions}</b> permission to access that page!', 'danger')
                return redirect(url_for('main.home')) if not fail_redirect else fail_redirect
            return func(*args, **kwargs)
        return wrapper
    return decorator
"""
