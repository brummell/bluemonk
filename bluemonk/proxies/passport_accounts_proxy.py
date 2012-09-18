from butterfly import PassportAccount

class PassportAccountsProxy(object):
    def __init__(self, butterfly):
        self.passport = PassportAccount(butterfly)

    def index(self, **options):
        return self.passport.get_passport_accounts(**options)

    def count(self, **options):
        return self.passport.get_passport_account_count(**options)

    def from_id(self, passport_account_id, **options):
        return self.passport.view_passport_account(passport_account_id, **options)
