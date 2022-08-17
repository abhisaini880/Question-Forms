from flask import request, Blueprint
from structlog import get_logger
from utils import Utility
from apis.question.schema import ADD_SCHEMA
from apis.question.model import Model
from apis.form.model import Model as FormModel

question_app = Blueprint("questions", __name__)
logger = get_logger("debug")


@question_app.route("", methods=["GET"])
def get():
    """
    Method to get the questions
    """
    return Utility.build_response(
        success=True, data=[], message="Fetched successfully!"
    )


@question_app.route("", methods=["POST"])
def post():
    """
    Method to create new question
    """

    try:
        question_request = Utility.payload_validator(
            schema=ADD_SCHEMA, payload=request.data
        )

        # check if form exists
        form = FormModel.get_form(form_id=question_request.get("form_id"))

        if not form:
            return Utility.build_response(
                success=False, data=[], message="Form doesn't exists"
            )

        question_count = form.get("questions_count", 0)
        existing_question_ids = form.get("questions", [])

        questions = []
        for question in question_request.get("questions", []):
            question_data = {
                "title": question.get("title"),
                "keyword": question.get("keyword"),
                "type": question.get("type"),
                "mandatory": question.get("mandatory"),
                "order": question.get("order"),
                "conditions": question.get("conditions"),
                # "created_by": g.user_data["user_id"], // will be implemented with the user management module.
            }
            question_count += 1
            questions.append(question_data)

        question_ids = Model.create_questions(questions)
        if not question_ids:
            return Utility.build_response(
                success=False,
                data=[],
                message="Unable to save questions !",
            )

        existing_question_ids.extend(question_ids)

        form_update_data = {
            "questions": existing_question_ids,
            "questions_count": question_count,
        }

        FormModel.update_form_by_id(
            form_id=question_request.get("form_id"),
            form_data=form_update_data,
        )

        form_update_data["questions"] = [
            str(question) for question in form_update_data["questions"]
        ]

        logger.info(form_update_data)

        return Utility.build_response(
            success=True, data=form_update_data, status_code=201
        )

    except Exception as error:
        logger.error(str(error))
        return Utility.build_response(success=False, data=[], status_code=400)


@question_app.route("/<question_id>", methods=["PUT"])
def put(question_id):
    """
    Update question
    """
    return Utility.build_response(
        success=True, data=[], message="updated successfully!"
    )
