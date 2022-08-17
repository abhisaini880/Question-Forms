from os import environ
from json import loads

MONGO = loads(environ.get("MONGO", "{}"))  # Expected dict
APPS_QUEUE = environ.get("APPS_QUEUE")
GOOGLE_CLIENT_KEYS = loads(
    environ.get("GOOGLE_CLIENT_KEYS", "{}")
)  # Expected dict
