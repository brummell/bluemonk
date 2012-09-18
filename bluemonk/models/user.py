from bluemonk.database import Model
from sqlalchemy import Column, Boolean, Integer, String, DateTime, ForeignKey, event

roles = {1: 'admin', 2:'support', 3:'helpdesk', 4:'hotel'}
class User(Model):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    openid = Column(String(200))
    name = Column(String(200))
    email = Column(String(200))
    role = Column(Integer)
    active = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    verification_token = Column(String(36))

    def __init__(self, openid, name, email):
        self.name = name
        self.openid = openid
        self.email = email
        self.role_name = None

    def generate_verification_token(self):
        import uuid
        self.verification_token = str(uuid.uuid4())

    def to_json(self):
        return dict(name=self.name, email=self.email, role=roles.get(self.role, None))

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

def load_monitor(target, context):
    if target.role:
        target.role_name = roles.get(target.role, None)

event.listen(User, 'load', load_monitor)
