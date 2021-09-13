""" Flask configuration variables """
from os import environ
from dotenv import load_dotenv

# Load environment variables from file .env
load_dotenv()

class Config:
    """ Set Flask configuration from .env file """

    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')

    TESTING = environ.get('TESTING')