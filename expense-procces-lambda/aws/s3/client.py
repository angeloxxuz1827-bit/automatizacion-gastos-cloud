import json
import boto3
from botocore.exceptions import ClientError


class S3Client:
    """
    Client responsible for interacting with Amazon S3.

    This class provides utility methods for storing and retrieving
    JSON objects from S3 buckets.
    """

    def __init__(self):
        """
        Initializes the Amazon S3 client.
        """

        # Create a boto3 S3 client instance.
        self.client = boto3.client("s3")

    def put_json(self, bucket: str, key: str, data: dict) -> None:
        """
        Uploads a JSON object to an Amazon S3 bucket.

        Args:
            bucket: Name of the destination S3 bucket.
            key: Object key (path) where the JSON will be stored.
            data: Dictionary to be serialized and uploaded as JSON.
        """

        # Upload the serialized JSON object to S3.
        self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False),
            ContentType="application/json"
        )

    def get_json(self, bucket: str, key: str) -> dict:
        """
        Retrieves and deserializes a JSON object from Amazon S3.

        Args:
            bucket: Name of the S3 bucket.
            key: Object key (path) of the JSON file.

        Returns:
            A dictionary containing the JSON content stored in S3.
        """

        # Retrieve the object from S3.
        response = self.client.get_object(
            Bucket=bucket,
            Key=key
        )

        # Read, decode, and deserialize the JSON content.
        return json.loads(
            response["Body"].read().decode("utf-8")
        )