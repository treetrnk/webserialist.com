import re
from math import floor
from flask import current_app, flash
from flask_login import current_user
from markdown import markdown

def round_half_up(n, decimals=0):
        multiplier = 10 ** decimals
        return floor(n*multiplier + 0.5) / multiplier

def format_hour_length(length):
    timelist = re.split("[^\d.]+", str(length))
    #print("TIMELIST: " + str(timelist))
    if len(timelist) == 4:
        hours = (int(timelist[0]) * 24) + int(timelist[1])
        formatted = hours + float(timelist[2]) / 60 + float(timelist[3]) / 60 / 60
    else:
        formatted = int(timelist[0]) + float(timelist[1]) / 60 + float(timelist[2]) / 60 / 60 
    return round_half_up(formatted, 2)

def convert_to_dict(obj):
    if type(obj) is not dict:
        data = {'repr': repr(obj)}
        for field in obj.__table__.columns:
            data[field.key] = obj.__dict__.get(field.key)
        #for field in obj.__table__.foreign_keys:
        #    data[field.key] = repr(obj.__dict__.get(field.key))
        try:
            data["users"] = obj.users
        except:
            pass
        try:
            data["user"] = obj.user
        except:
            pass
        try:
            data["groups"] = obj.groups
        except:
            pass
        try:
            data["permissions"] = obj.permissions
        except:
            pass
        try:
            data["creator"] = obj.creator
        except:
            pass
        try:
            data["editor"] = obj.editor
        except:
            pass
        try:
            data["parent"] = obj.parent
        except:
            pass
        try:
            data["category"] = obj.category
        except:
            pass
        return data
    return obj

def log_new(obj, message=''):
    data = convert_to_dict(obj)
    output = f'{current_user.username} {message}:\n'
    for key, value in data.items():
        output += f"    {key}: {value}\n"
    #print(output)
    current_app.logger.info(output)
    return True

def log_change(original, updated=None, message='changed something'):
    original_data = convert_to_dict(original)
    if updated:
        output = f'{current_user.username} {message}:\n'
        output += f"Changed object: {original['repr']}\n"
        updated_data = convert_to_dict(updated)
        for key, value in original_data.items():
            if key != 'repr':
                if key not in updated_data or value != updated_data[key]:
                    output += f'    {key}: {value}  ===CHANGED TO===>  {updated_data[key]}\n'
        #print(output)
        current_app.logger.info(output)
        return True
    return original_data
    
def log_form(form_obj):
    for field in form_obj:
        current_app.logger.debug(f'{field.name}: {field.data}')
        for error in field.errors:
            current_app.logger.warning(f'{field.name}: {error}')

def flash_form_errors(form_obj):
    if form_obj.errors:
        msg = """A problem occured with the following fields. 
                Please correct them and try again. 
                <ul>"""
        for error in form_obj.errors:
            msg += f"<li>{error}</li>"
    
        flash(msg, 'danger')

