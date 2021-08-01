import os
from os.path import join, dirname
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config(object):
    """ Production Configuration """
    BASE_DIR = Path('.')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class DevelopmentConfiguration(Config):
    """ Development Configuration """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

class TestingConfiguration(Config):
    """ Testing Configuration """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI  = os.getenv('DATABASE_URI_TEST')


app_configuration = {
    'production': Config,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}
