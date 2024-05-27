import os
import boto3
from botocore.exceptions import NoCredentialsError


class S3Helper:
    def __init__(self, access_key, secret_key, bucket_name):
        self.s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.bucket_name = bucket_name

    def upload_file(self, file_path: str):
        try:
            file = open(file_path, 'rb')
            self.s3_client.upload_fileobj(file, self.bucket_name, file_path)
            return True
        except NoCredentialsError:
            raise Exception("S3 credentials are not valid")

    def get_file(self, file_name: str, save_path: str = "temp"):
        try:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            with open(f"{save_path}/{file_name.split('/')[-1]}", 'wb') as f:
                f.write(response['Body'].read())
            return f"{save_path}/{file_name.split('/')[-1]}"
        except Exception as e:
            raise Exception(str(e))


