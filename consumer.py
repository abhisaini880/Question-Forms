""" Fetch data from SQS and call the service interface with the message data"""
import os
import boto3
from json import loads
from services.interface import InterfaceFactory

sqs_client = boto3.client("sqs", region_name="us-west-2")

queue_url = f"https://sqs.us-west-2.amazonaws.com/0000000000/{os.environ.get('APPS_QUEUE', '')}"


if __name__ == "__main__":
    while True:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
        )
        messages = response.get("Messages")
        for message in messages:
            try:
                message_body = loads(message.get("Body"))

                # Get the service based on app code
                app_data = message_body.get("app_data")
                app_code = app_data.get("app_code")
                service = InterfaceFactory(app_code)

                # call the process method
                service.process(message_body)

            except Exception as e:
                print(f"exception while processing message: {repr(e)}")
                continue
            message.delete()
            sqs_client.delete_message(
                QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
