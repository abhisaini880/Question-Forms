from flask import Flask
from dotenv import load_dotenv

from connectors.mongo import MongoDB
from connectors.google_sheet import GoogleSheet

# import blueprints
from apis.form.controller import form_app
from apis.question.controller import question_app
from apis.response.controller import response_app

# load the config into environment variables
load_dotenv(".env")

# create flask app
APP = Flask(__name__)

# load config
APP.config.from_pyfile("settings.py")

# build connectors clients
mongo_db = MongoDB(APP.config["MONGO"])
gsheet_client = GoogleSheet(APP.config["GOOGLE_CLIENT_KEYS"])

with APP.app_context():
    APP.config["mongo_db"] = mongo_db.connection
    APP.config["gsheet_client"] = gsheet_client.client

# registering blueprint
APP.register_blueprint(form_app, url_prefix="/v1/forms")
APP.register_blueprint(question_app, url_prefix="/v1/questions")
APP.register_blueprint(response_app, url_prefix="/v1/responses")

if __name__ == "__main__":
    APP.run()
