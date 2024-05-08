"""Module to define storage class for mongoDB"""

import os


def get_mongo_db_port():
    """Returns mongo DB port as int or None."""
    mongo_db_port = os.getenv("MONGO_DB_PORT")
    if mongo_db_port:
        return int(mongo_db_port)

    return None


DEFAULT_MONGO_DB_HOST = "127.0.0.1"
DEFAULT_MONGO_DB_PORT = 27017

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") or "telemetry"
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_HOST = os.getenv("MONGO_DB_HOST")
MONGO_DB_PORT = get_mongo_db_port()

# if both host and port are not defined the use default mongo host and port
if not (MONGO_DB_HOST or MONGO_DB_PORT):
    MONGO_DB_HOST = DEFAULT_MONGO_DB_HOST
    MONGO_DB_PORT = DEFAULT_MONGO_DB_PORT

MONGO_ACCESS_PARAMS = {
    "db": MONGO_DB_NAME,
    "password": MONGO_DB_PASSWORD,
    "username": MONGO_DB_USERNAME,
    "port": MONGO_DB_PORT,
    "host": MONGO_DB_HOST,
    "uuidRepresentation": "standard",
}
