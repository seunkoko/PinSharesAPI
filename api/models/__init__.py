from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# import helpers
from .helper import PushID

# import models
from .users import Users
from .pins import Pins

def fancy_id_generator(mapper, connection, target):
    '''
    A function to generate unique identifiers on insert
    '''
    push_id = PushID()
    target.id = push_id.next_id()

# associate the listener function with models, to execute during the
# "before_insert" event
tables = [
    # put in models here
    Users,
    Pins
]

for table in tables:
    event.listen(table, 'before_insert', fancy_id_generator)
