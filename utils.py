"""Common utility functions module."""

import boto3
from flask import current_app as app
from structlog import get_logger
from json import JSONDecodeError, loads
from jsonschema import Draft7Validator, draft7_format_checker
from services.interface import InterfaceFactory

logger = get_logger("debug")


class Utility:
    """Encapsulation of common function which will be used across files."""

    @staticmethod
    def send_to_sqs(queue_name, sqs_message):
        try:
            if app.config["ENV"] != "dev":
                sqs = boto3.resource("sqs", region_name="us-west-2")
                queue = sqs.get_queue_by_name(QueueName=queue_name)
                queue.send_message(MessageBody=sqs_message)
            else:
                message_body = loads(sqs_message)
                # Get the service based on app code
                app_data = message_body.get("app_data")
                app_code = app_data.get("app_code")
                service = InterfaceFactory(app_code)

                # call the process method
                service.process(message_body)

            return True
        except Exception as error:
            logger.info("Some Error Occured")
            logger.exception(str(error))
            return False

    @staticmethod
    def payload_validator(
        schema, payload=None, params=None, raise_exception=True
    ):
        """validate JSON paylaod

        Parameters
        ----------
        payload : string
            request.data json object
        params: JSON object
            request.args json object
        schema : dict
            jsonschema compatible schema dict
        """
        # decode payload and compare it against provided schema
        request_payload = {}
        try:
            if params:
                request_payload = params.to_dict()
            elif payload:
                request_payload = loads(payload)

        except JSONDecodeError as err:
            message = "Unable to parse request JSON. Invalid request body!!"
            raise Exception(message) from err
        validator = Draft7Validator(
            schema, format_checker=draft7_format_checker
        )
        compiled_error_msgs = []
        for error in sorted(validator.iter_errors(request_payload), key=str):
            error_message = (
                error.schema["error"]
                if error.schema.get("error")
                else str(error.message)
            )
            for suberror in sorted(error.context, key=lambda e: e.schema_path):
                suberror_message = (
                    suberror.schema["error"]
                    if suberror.schema.get("error")
                    else str(suberror.message)
                )
                compiled_error_msgs.append(suberror_message)
            compiled_error_msgs.append(error_message)

        if compiled_error_msgs:
            if raise_exception:
                raise Exception(str(compiled_error_msgs))
            return str(compiled_error_msgs)
        return request_payload

    @staticmethod
    def build_response(success, data, message=None, status_code=200):
        return {
            "success": success,
            "data": data,
            "messgae": message,
        }, status_code
