from groups_proxy import GroupsProxy
from guests_proxy import GuestsProxy
from mails_proxy import MailsProxy
from navigators_proxy import NavigatorsProxy

# This is not yet exposed by butterfly
#from passport_accounts_proxy import PassportAccountsProxy

from printers_proxy import PrintersProxy
from printer_configurations_proxy import PrinterConfigurationsProxy
from rooms_proxy import RoomsProxy
from room_classes_proxy import RoomClassesProxy
from service_coupons_proxy import ServiceCouponsProxy
from service_groups_proxy import ServiceGroupsProxy
from service_options_proxy import ServiceOptionsProxy
from service_purchases_proxy import ServicePurchasesProxy
from stays_proxy import StaysProxy
from stay_printjobs_proxy import StayPrintjobsProxy
from technicians_proxy import TechniciansProxy

class Proxies(object):
    '''The proxy object implements lazy instance auto-loading.
    It receives a butterfly instance as argument and will bind all created
    proxies to it.
    '''
    def __init__(self, butterfly):
        self.butterfly = butterfly
        self._instances = {}
        self._classes = {
            'Groups': GroupsProxy,
            'Guests': GuestsProxy,
            'Mails': MailsProxy,
            'Navigators': NavigatorsProxy,
#            'PassportAccounts': PassportAccountsProxy,
            'Printers': PrintersProxy,
            'PrinterConfigurations': PrinterConfigurationsProxy,
            'Rooms': RoomsProxy,
            'RoomClasses': RoomClassesProxy,
            'ServiceCoupons': ServiceCouponsProxy,
            'ServiceGroups': ServiceGroupsProxy,
            'ServiceOptions': ServiceOptionsProxy,
            'ServicePurchases': ServicePurchasesProxy,
            'Stays': StaysProxy,
            'StayPrintjobs': StayPrintjobsProxy,
            'Technicians': TechniciansProxy
        }

    def __getattr__(self, name):

        instance = self._instances.get(name, None)
        if instance:
            return instance

        klass = self._classes.get(name, None)
        if klass is None:
            msg = "Proxy `%s` does not exists." % name
            raise AttributeError(msg)

        instance = klass(self.butterfly)
        self._instances[name] = instance
        return instance
