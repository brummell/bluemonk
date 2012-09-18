from flask import session, redirect, url_for, request, flash, g, jsonify, abort

from bluemonk.database import db_session
from bluemonk.models.user import User
from bluemonk.models.hotel import Hotel
from bluemonk.libs.blueprint import Blueprint
from bluemonk.libs.identity import helpdesk_permission

'''
This component overloads the Flask.render_template function to inject the
hotel_id provided by the route.

The hotel_url_wrapper.load_hotel decorator injects the hotel_id in the g
request variable.
'''
from bluemonk.components.hotel_url_wrapper import load_hotel, render_template

from bluemonk.forms.room_search import RoomSearchForm

from bluemonk.facades import stays_facade, navigators_facade, guests_facade, service_options_facade, service_groups_facade

mod = Blueprint('helpdesk', __name__, url_prefix='/helpdesk', required_permission=helpdesk_permission)

@mod.route('/')
def home():
    hotels = Hotel.query.order_by('name')
    return render_template('helpdesk/home.html', hotels=hotels)

@mod.route('/hotels/<hotel_id>/search')
@load_hotel
def search(hotel_id):
    facade = stays_facade.search()
    return render_template('helpdesk/search.html', **facade)

@mod.route('/hotels/<hotel_id>/groups/')
@load_hotel
def groups_index(hotel_id):
    groups = g.proxies.Groups.index()
    return render_template('helpdesk/groups/index.html', groups=groups)

@mod.route('/hotels/<hotel_id>/groups/<group_id>/view')
@load_hotel
def groups_view(hotel_id, group_id):
    facade=groups_facade.view(group_id)
    return render_template('helpdesk/groups/view.html', **facade)

@mod.route('/hotels/<hotel_id>/guests/<guest_id>/view')
@load_hotel
def guests_view(hotel_id, guest_id):
    facade = guests_facade.view(guest_id)
    return render_template('helpdesk/guests/view.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/<navigator_id>/view')
@load_hotel
def navigators_view(hotel_id, navigator_id):
    facade = navigators_facade.view(navigator_id)
    return render_template('helpdesk/navigators/view.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/<navigator_id>/room_move', methods=['GET', 'POST'])
@load_hotel
def navigators_room_move(hotel_id, navigator_id):
    facade = navigators_facade.room_move(navigator_id)
    if facade.successful:
        return redirect(url_for('.navigators_view', hotel_id=hotel_id, navigator_id=navigator_id))
    return render_template('helpdesk/navigators/room_move.html', **facade)

@mod.route('/ajax/hotels/<hotel_id>/navigators/<navigator_id>/controls', methods=['POST'])
@load_hotel
def ajax_navigators_controls(hotel_id, navigator_id):
    facade = navigators_facade.controls(navigator_id)
    return jsonify({'successful': facade.successful})

@mod.route('/hotels/<hotel_id>/service_groups/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/service_groups/page:<int:page>')
@load_hotel
def service_groups_index(hotel_id, page):
    facade = service_groups_facade.index(page)
    return render_template('helpdesk/service_groups/index.html', **facade)

@mod.route('/hotels/<hotel_id>/service_groups/<service_group_id>/view')
@load_hotel
def service_groups_view(hotel_id, service_group_id):
    facade = service_groups_facade.view(service_group_id)
    return render_template('helpdesk/service_groups/view.html', **facade)

@mod.route('/hotels/<hotel_id>/service_options/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/service_options/page:<int:page>')
@load_hotel
def service_options_index(hotel_id, page):
    facade = service_options_facade.index(page)
    return render_template('helpdesk/service_options/index.html', **facade)

@mod.route('/hotels/<hotel_id>/service_options/<service_option_id>/view')
@load_hotel
def service_options_view(hotel_id, service_option_id):
    facade = service_options_facade.view(service_option_id)
    return render_template('helpdesk/service_options/view.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/')
@load_hotel
def stays_index(hotel_id):
    facade = stays_facade.index(page)
    return render_template('helpdesk/stays/index.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/view')
@load_hotel
def stays_view(hotel_id, stay_id):

    facade = stays_facade.view(stay_id)
    if not facade:
        return render_template('helpdesk/stays/index_no_stays.html', **facade)
    return render_template('helpdesk/stays/view.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/print_queue')
@load_hotel
def stays_print_queue(hotel_id, stay_id):
    facade = stays_facade.print_queue(stay_id)

    return render_template('helpdesk/stays/print_queue.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/printqueue/<item_id>', methods=['POST'])
@load_hotel
def stays_print_queue_actions(hotel_id, stay_id, item_id):
    facade = stays_facade.print_queue_actions(stay_id, item_id)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/purchases')
@load_hotel
def stays_purchases(hotel_id, stay_id):
    facade = stays_facade.purchases(stay_id)
    return render_template('helpdesk/stays/purchases.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/add_purchase', methods=['GET', 'POST'])
@load_hotel
def stays_add_purchase(hotel_id, stay_id):
    facade = stays_facade.add_purchase(stay_id)
    if facade.successful:
        return redirect(url_for('.stays_purchases', hotel_id=hotel_id, stay_id=stay_id))
    return render_template('helpdesk/stays/add_purchase.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/by_room_number', methods=['POST'])
@load_hotel
def stays_by_room_number(hotel_id):

    facade = stays_facade.by_room_number()
    if facade.empty_results:
        return redirect(url_for('.search', hotel_id=hotel_id))
    if not facade.successful:
        return render_template('helpdesk/search.html', **facade)
    if len(facade['stays']) == 1:
        return redirect(url_for('.stays_view', hotel_id=hotel_id, stay_id=facade['stays'][0]['Stay']['id']))

    return render_template('helpdesk/stays/by_room_number.html', **facade)
