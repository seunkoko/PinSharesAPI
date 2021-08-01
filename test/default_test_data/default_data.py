from datetime import datetime

from api.models import (
    Users, Pins
)

def create_default_users():
    user1 = Users(username="user1")
    user1.set_password('password1')

    user2 = Users(username="user2")
    user2.set_password('password2')

    user3 = Users(username="user3")
    user3.set_password('password3')

    user1.save()
    user2.save()
    user3.save()

def create_default_pins():
    user1 = Users.find_first(**{"username": "user1"})
    user2 = Users.find_first(**{"username": "user2"})
    user3 = Users.find_first(**{"username": "user3"})

    pin1 = Pins(
        user_id=user1.id,
        name="Pin 1",
        latLng=[1.0, 2.0]
    )

    pin2 = Pins(
        user_id=user2.id,
        name="Pin 2",
        latLng=[3.0, 4.0]
    )

    pin3 = Pins(
        user_id=user3.id,
        name="Pin 3",
        latLng=[5.0, 6.0]
    )

    pin4 = Pins(
        user_id=user1.id,
        name="Pin 1.1",
        latLng=[7.0, 8.0]
    )

    pin1.save()
    pin2.save()
    pin3.save()
    pin4.save()
