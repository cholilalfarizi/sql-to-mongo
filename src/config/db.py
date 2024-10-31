import mysql.connector
from . import config

def get_connection_db():
    return mysql.connector.connect(
        host=config.HOST_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
    )
