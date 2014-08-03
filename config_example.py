# config-example.py

# # Imports

import os

# # Flask

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# # Google APIs

SERVER_KEY = "<INSERT_KEY>"
BROWSER_KEY = "<INSERT_KEY>"

# # PostgreSQL

SF_MOVIES_USER = "<INSERT_USERNAME>"
SF_MOVIES_PASSWORD = "<INSERT_PASSWORD>"
SF_MOVIES_HOST = "<INSERT_DATABASE_HOST>"
SF_MOVIES_DATBASE = "<INSERT_DATABASE_NAME>"

# # SQLAlchemy

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://" + SF_MOVIES_USER + \
                              ":" + SF_MOVIES_PASSWORD + \
                              "@" + SF_MOVIES_HOST + \
                              "/" + SF_MOVIES_DATBASE
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
