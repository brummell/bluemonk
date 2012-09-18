from collections import namedtuple
from functools import partial

from bluemonk import principals

from flask.ext.principal import Permission, RoleNeed, UserNeed

user_permission = Permission(RoleNeed('user'))

admin_permission = Permission(RoleNeed('admin'))

support_permission = Permission(RoleNeed('support'))

helpdesk_permission = Permission(RoleNeed('helpdesk'))

hotel_permission = Permission(RoleNeed('hotel'))

HotelNeed = namedtuple('hotel', ['method', 'value'])
AccessHotelNeed = partial(HotelNeed, 'view')
