import sqlalchemy
import os
from flask_sqlalchemy import SQLAlchemy

db_user = os.environ.get('DB_USER_NAME')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')

db_url = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
db = SQLAlchemy()