def get_bucket_and_key(event: dict) -> tuple[str, str]:
    """
    Extrae el bucket y la key desde un evento de S3.
    """

    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    return bucket, key