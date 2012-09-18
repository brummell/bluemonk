from bluemonk.database import Model
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Hotel(Model):
    __tablename__ = 'hotels'
    id = Column('id', String(36), primary_key=True)
    name = Column(String(200))
    shorthand = Column(String(5))
    butterfly_user = Column(String(20))
    butterfly_token = Column(String(40))
    butterfly_url = Column(String(200))
    cups_password = Column(String(200))
    cups_address = Column(String(200))

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def validate_butterfly(self):
        if not self.butterfly_url:
            return False

        if not self.butterfly_url.startswith('http'):
            return False

        if len(self.butterfly_user) == 0 or len(self.butterfly_token) == 0:
            return False

        return True

    def to_json(self):
        items = dict(
            id=self.id,
            name=self.name,
        )
        return items

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)
