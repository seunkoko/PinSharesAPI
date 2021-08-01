import os
import logging

from flask_script import Manager, Server, prompt_bool, Shell
from flask_migrate import MigrateCommand
from logging.handlers import RotatingFileHandler
from sqlalchemy.exc import SQLAlchemyError

try:
    from server import create_flask_app
    from api.models import db
except ImportError:
    from .server import create_flask_app
    from .api.models import db

environment = os.getenv("FLASK_CONFIG")
app = create_flask_app(environment)

app.secret_key = os.getenv("APP_SECRET")

port = int(os.environ.get('PORT', 5000))
server = Server(host="0.0.0.0", port=port)


# initialize flask script
manager = Manager(app)

# enable migration commands
manager.add_command("runserver", server)
manager.add_command("db", MigrateCommand)


# initialize the log handler
handler = RotatingFileHandler('errors.log', maxBytes=10000000, backupCount=5)
formatter = logging.Formatter("%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
# set the log handler level
handler.setLevel(logging.INFO)
# set the app logger level
app.logger.setLevel(logging.INFO)
werkzeug_handler = logging.getLogger('werkzeug')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.addHandler(werkzeug_handler)

manager.run()
