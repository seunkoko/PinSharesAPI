from datetime import datetime
from sqlalchemy.orm import relationship

from .model_mixin import ModelMixin
from . import db, Users, Pins


class PinShares(ModelMixin):
    """ PinShares Table
        - Contains references to all shared pins and users
    """

    __tablename__ = 'pinshares'

    id = db.Column(db.String, primary_key=True) # primary key

    pin_id = db.Column(db.String, db.ForeignKey(Pins.id), nullable=False)

    # reference to user that shared and user share to
    shared_by = db.Column(db.String, db.ForeignKey(Users.id), nullable=False)
    shared_to = db.Column(db.String, db.ForeignKey(Users.id), nullable=False)
    
    # naming relationships for easy query
    by_user = relationship("Users", foreign_keys=shared_by)
    to_user = relationship("Users", foreign_keys=[shared_to], backref="shares")

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr_(self):
        return "<PinShares %r>" % (self.pin_id)