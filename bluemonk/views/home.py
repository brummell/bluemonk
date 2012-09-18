from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort

from bluemonk.database import db_session
from bluemonk.models.user import User

# This blueprint does not provide url prefix!
mod = Blueprint('home', __name__)

@mod.route('/')
def index():
    return render_template('home/index.html')

@mod.route('/about/')
def about():
    return render_template('home/about.html')
