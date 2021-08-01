from datetime import datetime
from sqlalchemy.dialects import postgresql

from .model_mixin import ModelMixin
from . import db, Users


class Pins(ModelMixin):
    """ Pins Table
        - Contains all Pins
    """

    __tablename__ = 'pins'

    id = db.Column(db.String, primary_key=True) # primary key

    # foreign key to the User's Table
    user_id = db.Column(db.String, db.ForeignKey(Users.id), nullable=False)

    name = db.Column(db.String, nullable=False)
    latLng = db.Column(postgresql.ARRAY(db.Float()), nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Pins %r>" % (self.name)

