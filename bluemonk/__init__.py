from flask import Flask, session, g, render_template, current_app, request
app = Flask(__name__)

# Hack for current Flask-principal to skip on static paths
#app.static_path = '/static/'
app.config.from_object('websiteconfig')

#Sessions
from bluemonk.libs.redis_sessions import RedisSessionInterface
app.session_interface = RedisSessionInterface()

#OpenID
from flask.ext.openid import OpenID
from bluemonk.libs.openid_store import DatabaseOpenIDStore
oid = OpenID(app, store_factory=DatabaseOpenIDStore)

# Asynchronous processing
from bluemonk.celery import celery

#Mails
from bluemonk.libs.mailer import Mailer
mailer = Mailer(app)

#Identity
from flask.ext.principal import Principal, PermissionDenied
principals = Principal(app, skip_static=True)

#cups error
from bluemonk.proxies.printers_proxy import CupsError

@app.errorhandler(CupsError)
def handle_cups_error(error):
    referrer = request.referrer
    return render_template('cups_error.html', error = error, referrer=referrer), 500

@app.errorhandler(PermissionDenied)
def handle_permission_error(error):
    #TODO Log permission error
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.before_request
def load_hotel():
    g.hotel_id = None
    g.hotel = None

@app.before_request
def load_current_user():
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()
    else:
        g.user = None

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()

@app.route('/hotel_misconfigured/<hotel_id>')
def hotel_misconfigured(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    return render_template('hotel_misconfigured.html', hotel=hotel)

from bluemonk.database import db_session
from bluemonk.models import User, Hotel
from bluemonk.views import authentication, profile, home, helpdesk, admin, tasks

app.register_blueprint(home.mod)
app.register_blueprint(authentication.mod)
app.register_blueprint(profile.mod)
app.register_blueprint(helpdesk.mod)
app.register_blueprint(admin.mod)
app.register_blueprint(tasks.mod)

from bluemonk.helpers import openid_helper, guest_helper, language_helper, paginator_helper, money_helper, badges_helper, text_helper
