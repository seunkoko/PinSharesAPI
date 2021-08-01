from datetime import datetime
from enum import unique
from sqlalchemy.orm import backref

from werkzeug.security import generate_password_hash, check_password_hash

from .model_mixin import ModelMixin
from . import db


class Users(ModelMixin):
    """ Users Table """

    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True) # primary key

    username = db.Column(db.String, nullable=False, unique=True) # unique
    password_hash = db.Column(db.String(128), nullable=False)

    my_pins = db.relationship(
        "Pins",
        backref="user",
        order_by="Pins.created_at.desc()",
        lazy=True
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Users %r>" % (self.username)

    def set_password(self, password):
        """ Hash user's password """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Confirm user's password """
        return check_password_hash(self.password_hash, password)

