from flask import render_template, session, redirect, url_for, request, flash, g, jsonify, abort

from bluemonk.database import db_session
from bluemonk.models.user import User, roles
from bluemonk.libs.identity import user_permission
from bluemonk.libs.blueprint import Blueprint

# This blueprint does not provide url prefix!
mod = Blueprint('profile', __name__, url_prefix='/profile', required_permission=user_permission)

@mod.route('/')
def view():
    env = dict(user=g.user, roles=roles)
    return render_template('profile/view.html', **env)

@mod.route('/update', methods=['GET', 'POST'])
def edit():
    return render_template('profile/edit.html')
