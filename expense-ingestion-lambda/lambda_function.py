import json

from aws.s3.client import S3Client
from aws.s3.key_builder import telegram_key
from config.settings import BUCKET_NAME

# Initialize the Amazon S3 client.
s3 = S3Client()


def lambda_handler(event, context):
    """
    AWS Lambda entry point for processing incoming Telegram webhook requests.

    This function receives the Telegram update from API Gateway,
    generates the corresponding S3 object key, stores the raw
    payload in Amazon S3, and returns a successful HTTP response.

    Args:
        event: AWS Lambda event containing the API Gateway request.
        context: AWS Lambda runtime context.

    Returns:
        A dictionary containing the HTTP status code and response body.
    """

    # Parse the JSON payload received from API Gateway.
    body = json.loads(event["body"])

    # Generate the S3 object key for the raw Telegram message.
    key = telegram_key(body, "raw")

    # Store the raw Telegram payload in Amazon S3.
    s3.put_json(
        bucket=BUCKET_NAME,
        key=key,
        data=body
    )

    # Return a successful HTTP response.
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"})
    }