from structlog import get_logger
from bson.objectid import ObjectId
from flask import current_app as app

logger = get_logger("debug")


class Model:
    @staticmethod
    def create_form(form_data):
        """
        Create new form entry

        Args:
            form_data (dict): new form data
        """

        try:
            form_insert_response = app.config["mongo_db"]["forms"].insert_one(
                form_data
            )

            return form_insert_response.inserted_id

        except Exception as error:
            logger.error(str(error))
            return None

    @staticmethod
    def get_form(form_id):
        """
        Get the form data based on id

        Args:
            form_id (string): form object id
        """
        try:
            query = {"_id": ObjectId(form_id)}
            form_data = app.config["mongo_db"]["forms"].find(query)
            logger.info(form_data)
            if form_data:
                form_data = form_data[0]
            return form_data
        except Exception as error:
            logger.error(str(error))
            return None

    @staticmethod
    def update_form_by_id(form_id, form_data):
        """
        update single form data

        Args:
            form_id (string): form object id
            form_data (dict): new form data
        """
        try:
            query = {"_id": ObjectId(form_id)}
            update_query = {"$set": form_data}

            app.config["mongo_db"]["forms"].update_one(query, update_query)

        except Exception as error:
            logger.error(str(error))
            return None
