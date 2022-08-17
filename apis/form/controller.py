from flask import Blueprint, request
from apis.form.schema import ADD_SCHEMA
from utils import Utility
from structlog import get_logger
from apis.form.model import Model

form_app = Blueprint("forms", __name__)
logger = get_logger("debug")


@form_app.route("", methods=["GET"])
def get():
    """
    Method to get the forms
    """
    return Utility.build_response(
        success=True, data=[], message="Fetched successfully!"
    )


@form_app.route("", methods=["POST"])
def post():
    """
    Method to create new form
    """

    try:
        form_request = Utility.payload_validator(
            schema=ADD_SCHEMA, payload=request.data
        )

        form_data = {
            "org_id": form_request.get("org_id"),
            "title": form_request.get("title"),
            # "created_by": g.user_data["user_id"], // will be implemented with the user management module.
            "active": True,
            "apps": form_request.get("apps"),
        }

        form_id = Model.create_form(form_data=form_data)
        logger.info(form_id)
        if not form_id:
            return Utility.build_response(
                success=False,
                data=[],
                message="Unable to save form !",
            )

        response_data = {"form_id": str(form_id)}

        return Utility.build_response(
            success=True, data=response_data, status_code=201
        )

    except Exception as error:
        logger.error(str(error))
        return Utility.build_response(success=False, data=[], status_code=400)


@form_app.route("/<form_id>", methods=["PUT"])
def put(form_id):
    """
    Update form
    """
    return Utility.build_response(
        success=True, data=[], message="Updated successfully!"
    )
