from flask import g
from bluemonk import app
from bluemonk.components.paginator import Paginator
from bluemonk.libs.facade import Facade
from bluemonk.forms.mail import MailForm

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    count = g.proxies.Mails.count()
    mails = g.proxies.Mails.index(page=page, limit=limit)
    paginator = Paginator(page, limit, count)
    facade = Facade(mails=mails,paginator=paginator)
    return facade

def view(mail_id, **options):
    mail = g.proxies.Mails.view(mail_id, **options)
    if not mail:
        abort(404)
    return Facade(mail=mail)

def add():
    groups = g.proxies.Groups.list()

    form = MailForm()
    form.recipients.choices = [('rooms', 'Rooms'), ('floors', 'Floors'), ('groups', 'Groups')]
    form.groups.choices = groups
    form.sender.choices = mail_sender_choices()

    facade = Facade(form=form)

    #TODO Move this to async as it will be slow.
    if form.validate_on_submit():
        # TODO Create the list of StaysMessage needed to link stays and messages
        data = form.data
        data['sender'] = mail_process_sender(data['sender'], form.sender.choices)
        mail = g.proxies.Mails.create(**data)
        facade.successful = True
        facade['mail_id'] = mail['StayMessage']['id']

    return facade

def mail_process_sender(sender, choices):
    '''
    Process the form data for the sender by swapping the form value to a
    printable one.
    '''

    sender = dict(choices).get(sender)
    if sender == 'me':
        return g.user.name
    return sender

def mail_sender_choices():
    '''
    Generates the available mail sender choices.
    '''

    #TODO Use Identity service

    choices = [('me', g.user.name)]
    if g.user.role == None:
        return choices

    if g.user.role == 4:
        choices.append(('hotel', 'Your Concierge'))

    if g.user.role <= 3:
        choices.append(('helpdesk', 'HCN Helpdesk'))
    if g.user.role <= 2:
        choices.append(('support', 'HCN Engineering'))
    if g.user.role == 1:
        choices.append(('admin', 'HCN'))

    return choices
