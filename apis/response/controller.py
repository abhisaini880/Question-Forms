from flask import request, Blueprint
from flask import current_app as app
from structlog import get_logger
from utils import Utility
from apis.response.schema import ADD_SCHEMA
from apis.response.model import Model
from apis.form.model import Model as FormModel
from json import dumps

response_app = Blueprint("responses", __name__)
logger = get_logger("debug")


@response_app.route("", methods=["GET"])
def get():
    """
    Method to get the response data
    """
    return Utility.build_response(
        success=True, data=[], message="fetched successfully!"
    )


@response_app.route("", methods=["POST"])
def post():
    """
    Method to submit new response
    """

    try:
        response_request = Utility.payload_validator(
            schema=ADD_SCHEMA, payload=request.data
        )

        # check if form exists
        form = FormModel.get_form(form_id=response_request.get("form_id"))

        if not form:
            return Utility.build_response(
                success=False, data=[], message="Form doesn't exists"
            )

        logger.info(form)

        integrated_apps = form.get("apps")

        response_data = {
            "form_id": response_request.get("form_id"),
            "response_time": response_request.get("response_time"),
            "user_meta": response_request.get("user_meta"),
            "answers": response_request.get("answers"),
            # "submitted_by": g.user_data["user_id"], // will be implemented with the user management module.
        }

        response_id = Model.create_response(response_data)
        if not response_id:
            return Utility.build_response(
                success=False,
                data=[],
                message="Unable to save response !",
            )

        # if integrated apps then send message to sqs.
        for app_data in integrated_apps:
            msg = dumps(
                {
                    "app_data": app_data,
                    "response_id": str(response_id),
                    "form_id": response_request.get("form_id"),
                }
            )

            Utility.send_to_sqs(
                queue_name=app.config.get("APPS_QUEUE"),
                sqs_message=msg,
            )

        response_data = {"response_id": str(response_id)}
        return Utility.build_response(
            success=True, data=response_data, status_code=201
        )

    except Exception as error:
        logger.error(str(error))
        return Utility.build_response(success=False, data=[], status_code=400)
