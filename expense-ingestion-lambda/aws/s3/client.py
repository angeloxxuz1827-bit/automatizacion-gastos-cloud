import json
import boto3
from botocore.exceptions import ClientError


class S3Client:

    def __init__(self):
        self.client = boto3.client("s3")

    def put_json(self, bucket: str, key: str, data: dict) -> None:
        self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False),
            ContentType="application/json"
        )

    def get_json(self, bucket: str, key: str) -> dict:
        response = self.client.get_object(
            Bucket=bucket,
            Key=key
        )

        return json.loads(
            response["Body"].read().decode("utf-8")
        )