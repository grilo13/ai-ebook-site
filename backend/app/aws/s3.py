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
                response = self.s3_client.upload_fileobj(f, self.bucket, file_name)
        except ClientError as e:
            logging.error(e)
            return False


if __name__ == '__main__':
    s3_client = S3(bucket='my-bucket', region='us-east-1')
    s3_client.upload_file(file_name="", file_path="")
