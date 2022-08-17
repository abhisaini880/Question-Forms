from structlog import get_logger
from flask import current_app as app


logger = get_logger("debug")


class Model:
    @staticmethod
    def create_questions(questions_data):
        """
        Create entry in question collection

        Args:
            question_data (dict): new question data
        """

        try:
            question_insert_response = app.config["mongo_db"][
                "questions"
            ].insert_many(questions_data)

            return question_insert_response.inserted_ids

        except Exception as error:
            logger.error(str(error))
            return None
