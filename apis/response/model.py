from structlog import get_logger
from bson.objectid import ObjectId
from flask import current_app as app


logger = get_logger("debug")


class Model:
    @staticmethod
    def create_response(response_data):
        """
        Create entry in response collection

        Args:
            response_data (dict): new response data
        """

        try:
            insert_response = app.config["mongo_db"]["responses"].insert_one(
                response_data
            )

            return insert_response.inserted_id

        except Exception as error:
            logger.error(str(error))
            return None

    @staticmethod
    def get_response(response_id):
        """
        Get the response data based on id

        Args:
            response_id (string): response object id
        """
        try:
            query = {"_id": ObjectId(response_id)}
            response_data = app.config["mongo_db"]["responses"].find(query)

            if response_data:
                response_data = response_data[0]

            return response_data
        except Exception as error:
            logger.error(str(error))
            return None
