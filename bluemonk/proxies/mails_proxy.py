from butterfly import StayMessage

class MailsProxy(object):
    def __init__(self, butterfly):
        self.mails = StayMessage(butterfly)

    def index(self, **options):
        return self.mails.get_mails(**options)

    def view(self, mail_id, **options):
        return self.mails.view_mail(mail_id, **options)

    def create(self, **data):
        return self.mails.add_mail(**data)

    def count(self, **options):
        count = self.mails.get_mail_count(**options)
        if not 'count' in count:
            return 0
        return int(count['count'])
