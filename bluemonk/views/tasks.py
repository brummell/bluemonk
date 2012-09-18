from flask import render_template, session, redirect, url_for, request, flash, g, jsonify, abort
from bluemonk import celery
from bluemonk.libs.blueprint import Blueprint
from bluemonk.libs.identity import admin_permission

mod = Blueprint('tasks', __name__, url_prefix='/admin/tasks', required_permission=admin_permission)

@mod.route('/')
def index():
    inspector = celery.control.inspect()
    tasks = dict(active=inspector.active(), scheduled=inspector.scheduled())
    return render_template('admin/tasks/index.html', **tasks)

@mod.route('/ping')
def ping():
    workers = celery.control.ping()
    return render_template('admin/tasks/ping.html', workers=workers)

@mod.route('/reload')
def reload():
    celery.control.broadcast('pool_restart', arguments={'reload': True})
    flash('Celery workers reloading...')
    return redirect(url_for('.index'))
