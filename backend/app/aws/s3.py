import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger('s3')


class S3:
    def __init__(self, bucket: str, region: str):
        self.s3_client = boto3.client("s3")
        self.bucket = bucket
        self.region = region

    def try_permissions(self):
        # Attempt to get S3 buckets
        # This operation doesn't change any settings, but will fail if credentials are not available
        self.s3_client.list_buckets()

    def upload_file(self, file_name: str, file_path: str):
        self.try_permissions()
        try:
            with open(file_path, "rb") as f:
                self.s3_client.upload_fileobj(f, self.bucket, file_name)
        except ClientError as e:
            logging.error(e)
            return False

        file_url = self._get_file_url(self.bucket, file_name)
        return file_url

    def _get_file_url(self, bucket_name: str, s3_file_name: str):
        file_url = f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{s3_file_name}"
        return file_url


if __name__ == '__main__':
    s3_client = S3(bucket='my-bucket', region='us-east-1')
    s3_client.upload_file(file_name="", file_path="")
