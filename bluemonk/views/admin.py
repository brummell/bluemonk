from flask import session, redirect, url_for, request, flash, g, jsonify, abort

from bluemonk import app, mailer
from bluemonk.database import db_session
from bluemonk.models.user import User, roles as user_roles
from bluemonk.models.hotel import Hotel
from bluemonk.libs.identity import admin_permission
from bluemonk.libs.blueprint import Blueprint
from bluemonk.emails.user_verification import UserVerificationMessage
import json

'''
This component overloads the Flask.render_template function to inject the
hotel_id provided by the route.

The hotel_url_wrapper.load_hotel decorator injects the hotel_id in the g
request variable.
'''
from bluemonk.components.hotel_url_wrapper import load_hotel, render_template
from bluemonk.components.paginator import Paginator

from bluemonk.forms.hotel import HotelForm, HotelDeleteForm
from bluemonk.forms.user import UserForm, UserSendVerificationForm, UserDeleteForm

from bluemonk.facades import *

mod = Blueprint('admin', __name__, url_prefix='/admin', required_permission=admin_permission)

@mod.route('/')
def home():
    hotels = Hotel.query.order_by('name')
    return render_template('admin/home.html', hotels=hotels)

@mod.route('/hotels/')
def hotels_index():
    hotels = Hotel.query.order_by('name')
    return render_template('admin/hotels/index.html', hotels=hotels)

@mod.route('/hotels/new', methods=['GET', 'POST'])
def hotels_add():
    form = HotelForm()
    if form.validate_on_submit():
        hotel = Hotel()
        form.populate_obj(hotel)
        db_session.add(hotel)
        db_session.commit()
        flash('Hotel added.', 'success')
        return redirect(url_for('.hotels_index'))

    return render_template('admin/hotels/add.html', form=form)

@mod.route('/hotels/<hotel_id>/edit', methods=['GET', 'POST'])
def hotels_edit(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        abort(404)

    form = HotelForm(obj=hotel)
    if form.validate_on_submit():
        form.populate_obj(hotel)
        db_session.commit()
        flash('Hotel information updated.', 'success')
        return redirect(url_for('.hotels_view', hotel_id=hotel.id))
    return render_template('admin/hotels/edit.html', form=form,hotel=hotel)

@mod.route('/hotels/<hotel_id>/delete', methods=['GET','POST'])
def hotels_delete(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        abort(404)

    form = HotelDeleteForm()
    if not form.validate_on_submit():
        abort(400)

    db_session.delete(hotel)
    db_session.commit()
    flash('Hotel deleted.', 'success')
    return redirect(url_for('.hotels_index'))

@mod.route('/hotels/<hotel_id>')
def hotels_view(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        abort(404)

    form = HotelDeleteForm(id = hotel.id)
    return render_template('admin/hotels/view.html', hotel=hotel, form=form)

@mod.route('/hotels/<hotel_id>/home')
@load_hotel
def hotel_home(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        abort(404)

    return render_template('admin/hotel/home.html', hotel=hotel)

@mod.route('/hotels/<hotel_id>/groups/')
@load_hotel
def groups_index(hotel_id):
    groups = g.proxies.Groups.index()
    return render_template('admin/hotel/groups/index.html', groups=groups)

@mod.route('/hotels/<hotel_id>/groups/<group_id>/view', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/groups/<group_id>/view/page:<int:page>')
@load_hotel
def groups_view(hotel_id, group_id, page):
    facade = groups_facade.view(group_id, page)
    return render_template('admin/hotel/groups/view.html', **facade)

@mod.route('/hotels/<hotel_id>/groups/new', methods=['GET','POST'])
@load_hotel
def groups_add(hotel_id):
    facade = groups_facade.add()
    if facade.successful:
        return redirect(url_for('.groups_view', group_id=facade['group_id']))

    return render_template('admin/hotel/groups/add.html', **facade)

@mod.route('/hotels/<hotel_id>/groups/<group_id>/edit', methods=['GET','POST'])
@load_hotel
def groups_edit(hotel_id, group_id):
    facade = groups_facade.edit(group_id)
    if facade.successful:
        return redirect(url_for('.groups_view', group_id=facade['group_id']))

    return render_template('admin/hotel/groups/add.html', **facade)

@mod.route('/hotels/<hotel_id>/groups/<group_id>/delete', methods=['POST'])
@load_hotel
def groups_delete(hotel_id, group_id):
    groups_facade.delete(group_id)
    return redirect(url_for('.groups_index'))

@mod.route('/hotels/<hotel_id>/groups/<group_id>/link_pms_groups', methods=['GET', 'POST'])
@load_hotel
def groups_add_pms_group(hotel_id, group_id):
    facade = groups_facade.link_pms_group(group_id)
    if facade.successful:
        return redirect(url_for('.groups_view', hotel_id=hotel_id, group_id = group_id))
    return render_template('admin/hotel/groups/link_pms_group.html', **facade)

@mod.route('/hotels/<hotel_id>/groups/<group_id>/unlink_pms_group', methods=['POST'])
@load_hotel
def groups_remove_pms_group(hotel_id, group_id):
    facade = groups_facade.unlink_pms_group(group_id)
    return redirect(url_for('.groups_view', hotel_id=hotel_id, group_id=group_id))

@mod.route('/hotels/<hotel_id>/guests/', defaults={'page' :1})
@mod.route('/hotels/<hotel_id>/guests/page:<int:page>')
@load_hotel
def guests_index(hotel_id, page):
    facade = guests_facade.index(page)
    return render_template('admin/hotel/guests/index.html', **facade)

@mod.route('/hotels/<hotel_id>/guests/<guest_id>/view')
@load_hotel
def guests_view(hotel_id, guest_id):
    facade = guests_facade.view(guest_id)
    return render_template('admin/hotel/guests/view.html', **facade)

@mod.route('/hotels/<hotel_id>/mails/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/mails/page:<int:page>')
@load_hotel
def mails_index(hotel_id, page):
    facade = mails_facade.index(page)
    return render_template('admin/hotel/mails/index.html', **facade)

@mod.route('/hotels/<hotel_id>/mails/add', methods=['GET', 'POST'])
@load_hotel
def mails_add(hotel_id):
    facade = mails_facade.add()
    if facade.successful:
        return redirect(url_for('.mails_view', hotel_id=hotel_id, mail_id=facade['mail_id']))
    return render_template('admin/hotel/mails/add.html', **facade)

@mod.route('/hotels/<hotel_id>/mails/<mail_id>/view')
@load_hotel
def mails_view(hotel_id, mail_id):
    facade = mails_facade.view(mail_id)
    return render_template('admin/hotel/mails/view.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/navigators/page:<int:page>')
@load_hotel
def navigators_index(hotel_id, page):
    facade = navigators_facade.index(page)
    return render_template('admin/hotel/navigators/index.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/<navigator_id>/view')
@load_hotel
def navigators_view(hotel_id, navigator_id):
    facade = navigators_facade.view(navigator_id)
    return render_template('admin/hotel/navigators/view.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/<navigator_id>/room_move', methods=['GET', 'POST'])
@load_hotel
def navigators_room_move(hotel_id, navigator_id):
    facade = navigators_facade.room_move(navigator_id)
    if facade.successful:
        return redirect(url_for('.navigators_view', hotel_id=hotel_id, navigator_id=navigator_id))
    return render_template('admin/hotel/navigators/room_move.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/add', methods=['GET', 'POST'])
@load_hotel
def navigators_add(hotel_id):
    facade = navigators_facade.add()
    if facade.successful:
        return redirect(url_for('.navigators_view', hotel_id=hotel_id, navigator_id=facade['navigator_id']))
    return render_template('admin/hotel/navigators/add.html', **facade)

@mod.route('/hotels/<hotel_id>/navigators/<navigator_id>/edit', methods=['GET', 'POST'])
@load_hotel
def navigators_edit(hotel_id, navigator_id):
    facade = navigators_facade.edit(navigator_id)
    if facade.successful:
        return redirect(url_for('.navigators_view', hotel_id=hotel_id, navigator_id=navigator_id))
    return render_template('admin/hotel/navigators/edit.html', **facade)

@mod.route('/ajax/hotels/<hotel_id>/navigators/<navigator_id>/controls', methods=['POST'])
@load_hotel
def ajax_navigators_controls(hotel_id, navigator_id):
    facade = navigators_facade.controls(navigator_id)
    return jsonify({'successful': facade.successful})

@mod.route('/ajax/hotels/<hotel_id>/stays/<stay_id>/controls/', methods=['POST'])
@load_hotel
def stay_controls(hotel_id, stay_id):
    facade = stays_facade.update(stay_id, request.form)
    
    return jsonify({'successful': facade}) 

@load_hotel
def passport_accounts_view(hotel_id, passport_account_id):
    facade = passport_accounts_facade.view(passport_account_id)
    return render_template('admin/hotel/passport_accounts/view.html', **facade)

@mod.route('/hotels/<hotel_id>/printers/')
@load_hotel
def printers_index(hotel_id):
    printers = g.proxies.Printers.index()
    return render_template('admin/hotel/printers/index.html', printers=printers)

@mod.route('/hotels/<hotel_id>/printers/jobs')
@load_hotel
def printers_jobs(hotel_id):
    jobs = g.proxies.Printers.get_jobs()
    return render_template('admin/hotel/printers/jobs.html', jobs=jobs)

@mod.route('/hotels/<hotel_id>/printers/jobs/<job_id>/cancel')
@load_hotel
def printers_cancel_job(hotel_id, job_id):
    g.proxies.Printers.cancel_job(job_id)
    jobs = g.proxies.Printers.get_jobs()
    return render_template('admin/hotel/printers/jobs.html', jobs=jobs)

@mod.route('/hotels/<hotel_id>/printers/<printer_id>/view')
@load_hotel
def printer_view(hotel_id, printer_id):
    printers = g.proxies.Printers.index()
    printer = printers[printer_id]
    print printer
    return render_template('admin/hotel/printers/view.html', printer_id=printer_id, printer=printer)

@mod.route('/hotels/<hotel_id>/printers/<printer_id>/enable')
@load_hotel
def printer_enable(hotel_id, printer_id):
    g.proxies.Printers.enable_printer(printer_id)
    printers = g.proxies.Printers.index()
    printer = printers[printer_id]
    return render_template('admin/hotel/printers/view.html', printer_id=printer_id, printer=printer)

@mod.route('/hotels/<hotel_id>/printers/<printer_id>/cancel_all_jobs')
@load_hotel
def printer_cancel_print_jobs(hotel_id, printer_id):
    g.proxies.Printers.cancel_all_jobs(printer_id)
    printers = g.proxies.Printers.index()
    printer = printers[printer_id]
    return render_template('admin/hotel/printers/view.html', printer_id=printer_id, printer=printer)

@mod.route('/hotels/<hotel_id>/printers/<printer_id>/disable')
@load_hotel
def printer_disable(hotel_id, printer_id):
    g.proxies.Printers.disable_printer(printer_id)
    printers = g.proxies.Printers.index()
    printer = printers[printer_id]
    return render_template('admin/hotel/printers/view.html', printer_id=printer_id, printer=printer)

@mod.route('/hotels/<hotel_id>/printer_configurations/')
@load_hotel
def printer_configurations_index(hotel_id):
    printerConfigurations = g.proxies.PrinterConfigurations.index()
    return render_template('admin/hotel/printer_configurations/index.html', printerConfigurations=printerConfigurations)

@mod.route('/hotels/<hotel_id>/printer_configurations/new', methods=['GET', 'POST'])
@load_hotel
def printer_configurations_add(hotel_id):
    facade = printer_configurations_facade.add()

    if 'printer_configuration_id' in facade:
        flash("Printer configuration added.", 'success')
        return redirect(url_for('.printer_configurations_index', hotel_id=hotel_id))

    return render_template('admin/hotel/printer_configurations/add.html', **facade)

@mod.route('/hotels/<hotel_id>/printer_configurations/<printer_configuration_id>/edit', methods=['GET', 'POST'])
@load_hotel
def printer_configurations_edit(hotel_id, printer_configuration_id):
    facade = printer_configurations_facade.edit(printer_configuration_id)

    if facade.successful:
        flash("Printer configuration updated.", 'success')
        return redirect(url_for('.printer_configurations_index', hotel_id=hotel_id))

    return render_template('admin/hotel/printer_configurations/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/stay_printjobs/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/stay_printjobs/page:<int:page>')
@load_hotel
def print_jobs_index(hotel_id, page):
    facade = stay_printjobs_facade.index(page)
    return render_template('admin/hotel/stay_printjobs/index.html', **facade)

@mod.route('/hotels/<hotel_id>/stay_printjobs/<print_job_id>/view')
@load_hotel
def print_jobs_view(hotel_id, stay_printjob_id):
    facade = stay_printjobs_facade.view(stay_printjob_id)
    return render_template('admin/hotel/stay_printjobs/index.html', **facade)

@mod.route('/hotels/<hotel_id>/rooms/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/rooms/page:<int:page>')
@load_hotel
def rooms_index(hotel_id, page):
    facade = rooms_facade.index(page)
    return render_template('admin/hotel/rooms/index.html', **facade)

@mod.route('/hotels/<hotel_id>/rooms/<room_id>/view')
@load_hotel
def rooms_view(hotel_id, room_id):
    facade = rooms_facade.view(room_id)
    return render_template('admin/hotel/rooms/view.html', **facade)

@mod.route('/hotels/<hotel_id>/rooms/<room_id>/edit', methods=['GET','POST'])
@load_hotel
def rooms_edit(hotel_id, room_id):
    facade = rooms_facade.edit(room_id)
    if facade.successful:
        return redirect(url_for('.rooms_view', hotel_id=hotel_id, room_id=facade['room_id']))
    return render_template('admin/hotel/rooms/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/rooms/add', methods=['GET','POST'])
@load_hotel
def rooms_add(hotel_id):
    facade = rooms_facade.add()
    if facade.successful:
        return redirect(url_for('.rooms_view', hotel_id=hotel_id, room_id=facade['room_id']))
    return render_template('admin/hotel/rooms/add.html', **facade)

@mod.route('/hotels/<hotel_id>/room_classes/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/room_classes/page:<int:page>')
@load_hotel
def room_classes_index(hotel_id, page):
    facade = room_classes_facade.index(page)
    return render_template('admin/hotel/room_classes/index.html', **facade)

@mod.route('/hotels/<hotel_id>/room_classes/add', methods=['GET','POST'])
@load_hotel
def room_classes_add(hotel_id):
    facade = room_classes_facade.create()
    if facade.successful:
        return redirect(url_for('.room_classes_index', hotel_id=hotel_id))
    return render_template('admin/hotel/room_classes/add.html', **facade)

@mod.route('/hotels/<hotel_id>/room_classes/<room_class_id>/edit', methods=['GET', 'POST'])
@load_hotel
def room_classes_edit(hotel_id, room_class_id):
    facade = room_classes_facade.update(room_class_id)
    if facade.successful:
        return redirect(url_for('.room_classes_index', hotel_id=hotel_id))
    return render_template('admin/hotel/room_classes/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/service_bundles/')
@load_hotel
def service_bundles_index(hotel_id):
    serviceBundles = g.proxies.ServiceBundles.index()
    return render_template('admin/hotel/service_bundles/index.html', serviceBundles=serviceBundles)

@mod.route('/hotels/<hotel_id>/service_coupons/', defaults={"page": 1})
@mod.route('/hotels/<hotel_id>/service_coupons/page:<int:page>')
@load_hotel
def service_coupons_index(hotel_id, page):
    facade = service_coupons_facade.index(page)
    return render_template('admin/hotel/service_coupons/index.html', **facade)

@mod.route('/hotels/<hotel_id>/service_coupons/<service_coupon_id>/view')
@load_hotel
def service_coupons_view(hotel_id, service_coupon_id):
    facade = service_coupons_facade.view(service_coupon_id)
    return render_template('admin/hotel/service_coupons/view.html', **facade)

@mod.route('/hotels/<hotel_id>/service_coupons/<service_coupon_id>/edit', methods=['GET','POST'])
@load_hotel
def service_coupons_edit(hotel_id, service_coupon_id):
    facade = service_coupons_facade.edit(service_coupon_id)
    if facade.successful:
        return redirect(url_for('.service_coupons_view', hotel_id=hotel_id, service_coupon_id=service_coupon_id))
    return render_template('admin/hotel/service_coupons/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/service_coupons/create', methods=['GET','POST'])
@load_hotel
def service_coupons_add(hotel_id):
    facade = service_coupons_facade.add()

    if facade.successful:
        return redirect(url_for('.service_coupons_view', hotel_id=hotel_id, service_coupon_id=facade['service_coupon_id']))

    return render_template('admin/hotel/service_coupons/add.html', **facade)

@mod.route('/hotels/<hotel_id>/service_coupons/<service_coupon_id>/edit', methods=['GET','POST'])
@load_hotel
def service_coupons_edit(hotel_id, service_coupon_id):
    facade = service_coupons_facade.edit(service_coupon_id)

    if facade.successful:
        return redirect(url_for('.service_coupons_view', hotel_id=hotel_id, service_coupon_id=facade['service_coupon_id']))

    return render_template('admin/hotel/service_coupons/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/service_coupons/<service_coupon_id>/view')
@load_hotel
def service_coupons_view(hotel_id, service_coupon_id):
    facade = service_coupons_facade.view(service_coupon_id)
    return render_template('admin/hotel/service_coupons/view.html', **facade)

@mod.route('/hotels/<hotel_id>/service_groups/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/service_groups/page:<int:page>')
@load_hotel
def service_groups_index(hotel_id, page):
    facade = service_groups_facade.index(page)
    return render_template('admin/hotel/service_groups/index.html', **facade)

@mod.route('/hotels/<hotel_id>/service_groups/<service_group_id>/view')
@load_hotel
def service_groups_view(hotel_id, service_group_id):
    facade = service_groups_facade.view(service_group_id)
    return render_template('admin/hotel/service_groups/view.html', **facade)

@mod.route('/hotels/<hotel_id>/service_groups/add', methods=['GET', 'POST'])
@load_hotel
def service_groups_add(hotel_id):
    facade = service_groups_facade.add()
    if facade.successful:
        return redirect(url_for('.service_groups_view', hotel_id=hotel_id, service_group_id=service_group_id))
    return render_template('admin/hotel/service_groups/add.html', **facade)

@mod.route('/hotels/<hotel_id>/service_groups/<service_group_id>/edit', methods=['GET', 'POST'])
@load_hotel
def service_groups_edit(hotel_id, service_group_id):
    facade = service_groups_facade.edit(service_group_id)
    if facade.successful:
        return redirect(url_for('.service_groups_view', hotel_id=hotel_id, service_group_id=service_group_id))
    return render_template('admin/hotel/service_groups/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/service_options/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/service_options/page:<int:page>')
@load_hotel
def service_options_index(hotel_id, page):
    facade = service_options_facade.index(page)
    return render_template('admin/hotel/service_options/index.html', **facade)

@mod.route('/hotels/<hotel_id>/service_options/<service_option_id>/view')
@load_hotel
def service_options_view(hotel_id, service_option_id):
    facade = service_options_facade.view(service_option_id)
    return render_template('admin/hotel/service_options/view.html', **facade)

@mod.route('/hotels/<hotel_id>/service_options/create', methods=['GET', 'POST'])
@load_hotel
def service_options_add(hotel_id):
    facade = service_options_facade.add()
    if facade.successful:
        return redirect(url_for('.service_options_view', hotel_id=hotel_id, service_option_id=facade['service_option_id']))
    return render_template('admin/hotel/service_options/add.html', **facade)

@mod.route('/hotels/<hotel_id>/service_options/<service_option_id>/edit', methods=['GET', 'POST'])
@load_hotel
def service_options_edit(hotel_id, service_option_id):
    facade = service_options_facade.edit(service_option_id)
    if facade.successful:
        return redirect(url_for('.service_options_view', hotel_id=hotel_id, service_option_id=facade['service_option_id']))
    return render_template('admin/hotel/service_options/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/service_purchases/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/service_purchases/page:<int:page>')
@load_hotel
def service_purchases_index(hotel_id, page):
    facade = service_purchases_facade.index(page)
    return render_template('admin/hotel/service_purchases/index.html', **facade)

@mod.route('/hotels/<hotel_id>/service_purchases/<service_purchase_id>/view')
@load_hotel
def service_purchases_view(hotel_id, service_purchase_id):
    facade =service_purchases_facade.view(service_purchase_id)
    return render_template('admin/hotel/service_purchases/view.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/by_room_number', methods=['POST'])
@load_hotel
def stays_by_room_number(hotel_id):

    facade = stays_facade.by_room_number()
    if facade.empty_results:
        return redirect(url_for('.stays_search', hotel_id=hotel_id))
    if not facade.successful:
        return render_template('admin/hotel/stays/search.html', **facade)
    if len(facade['stays']) == 1:
        return redirect(url_for('.stays_view', hotel_id=hotel_id, stay_id=facade['stays'][0]['Stay']['id']))

    return render_template('admin/hotel/stays/by_room_number.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/', defaults={'page': 1})
@mod.route('/hotels/<hotel_id>/stays/page:<int:page>')
@load_hotel
def stays_index(hotel_id, page):
    facade = stays_facade.index(page)
    return render_template('admin/hotel/stays/index.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/search')
@load_hotel
def stays_search(hotel_id):
    facade = stays_facade.search()
    return render_template('admin/hotel/stays/search.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/view')
@load_hotel
def stays_view(hotel_id, stay_id):
    facade = stays_facade.view(stay_id)
    if not facade:
        return render_template('admin/hotel/stays/no_stay.html')
    facade["hotel_id"] = hotel_id
    #raise Exception(str( facade))
    return render_template('admin/hotel/stays/view.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/print_queue')
@load_hotel
def stays_print_queue(hotel_id, stay_id):
    facade = stays_facade.print_queue(stay_id)
    return render_template('admin/hotel/stays/print_queue.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/printqueue/<item_id>', methods=['POST'])
@load_hotel
def stays_print_queue_actions(hotel_id, stay_id, item_id):
    facade = stays_facade.print_queue_actions(stay_id, item_id)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/purchases')
@load_hotel
def stays_purchases(hotel_id, stay_id):
    facade = stays_facade.purchases(stay_id)
    return render_template('admin/hotel/stays/purchases.html', **facade)

@mod.route('/hotels/<hotel_id>/stays/<stay_id>/add_purchase', methods=['GET', 'POST'])
@load_hotel
def stays_add_purchase(hotel_id, stay_id):
    facade = stays_facade.add_purchase(stay_id)
    if facade.successful:
        return redirect(url_for('.stays_purchases', hotel_id=hotel_id, stay_id=stay_id))
    return render_template('admin/hotel/stays/add_purchase.html', **facade)

@mod.route('/hotels/<hotel_id>/technicians/')
@load_hotel
def technicians_index(hotel_id):
    technicians = g.proxies.Technicians.index()
    return render_template('admin/hotel/technicians/index.html', technicians=technicians)

@mod.route('/hotels/<hotel_id>/technicians/add', methods=['GET', 'POST'])
@load_hotel
def technicians_add(hotel_id):
    facade = technicians_facade.add()
    if facade.successful:
        return redirect(url_for('.technicians_index'))

    return render_template('admin/hotel/technicians/add.html', **facade)

@mod.route('/hotels/<hotel_id>/technicians/<technician_id>/edit', methods=['GET', 'POST'])
@load_hotel
def technicians_edit(hotel_id, technician_id):
    facade = technicians_facade.edit(technician_id)
    if facade.successful:
        return redirect(url_for('.technicians_index', hotel_id=hotel_id))

    return render_template('admin/hotel/technicians/edit.html', **facade)

@mod.route('/hotels/<hotel_id>/technicians/<technician_id>/delete', methods=['POST'])
@load_hotel
def technicians_delete(hotel_id, technician_id):
    g.proxies.technician.delete_technician(technician_id)
    return redirect(url_for('admin/hotel/technicians/'))

@mod.route('/users/')
def users_index():
    users = User.query.order_by('name')
    form = UserDeleteForm()
    return render_template('admin/users/index.html', users=users, form=form)

@mod.route('/users/<user_id>/edit', methods=['POST','GET'])
def users_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)

    user_form = UserForm(obj=user)

    verification_form = UserSendVerificationForm(obj=user)
    if user_form.validate_on_submit():
        user_form.populate_obj(user)
        db_session.commit()
        return redirect(url_for('.users_index'))

    return render_template('admin/users/edit.html', user=user, user_form=user_form, verification_form=verification_form)

@mod.route('/users/delete', methods=['POST'])
def users_delete():
    form = UserDeleteForm()
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        flash('The user does not exists.')
    else:
        if form.validate_on_submit:
            db_session.delete(user)
            db_session.commit()
            flash('The user has been deleted')
    return redirect(url_for('.users_index'))

@mod.route('/users/<user_id>/send_verification', methods=['POST'])
def users_send_verification(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.verified = False
    user.generate_verification_token()
    db_session.commit()

    mailer.send(UserVerificationMessage, to=user.email, user_id=user.id, verification_token=user.verification_token)
    flash('Email verification sent to %s' % user.email, 'success')
    return redirect(url_for('.users_index'))

