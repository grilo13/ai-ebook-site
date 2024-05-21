import boto3
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv

logger = logging.getLogger('s3')

load_dotenv()


class S3:
    def __init__(self, bucket: str, region: str):
        self.s3_client = boto3.client("s3")
        self.bucket = bucket
        self.region = region

    def try_permissions(self):
        # Attempt to get S3 buckets
        # This operation doesn't change any settings, but will fail if credentials are not available
        buckets = self.s3_client.list_buckets()
        print("buckets {}".format(buckets))

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
    s3_client = S3(bucket='ai-new', region='eu-north-1')
    file_url = s3_client.upload_file(file_name="preview_photo.png", file_path="../models/preview_photo.png")
    # file_url = s3_client._get_file_url(bucket_name='ai-new', s3_file_name='teste-9a65815a-5d9b-4fe9-9a98-06efd3484c80.docx')
    print("file_url:", file_url)
