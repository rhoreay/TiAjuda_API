from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

# load environment variables from .env 
load_dotenv()

db = SQLAlchemy()

# database connection string
SQLALCHEMY_CONNECTION_STRING = f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DATABASE")}'

# creating request limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=f'mongodb://{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/{os.getenv("MONGODB_DATABASE")}'
)

# parse whitelist ips from .env
ip_whitelist = os.getenv("WHITELIST_IPS").split(',')
