import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def get_file(key):
    """Retrieves the content of a file from an S3 bucket."""
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    try:
        response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                 Key=key)
        return response['Body'].read().decode('utf-8')
    except ClientError as e:
        return ''


def upload_file(file, key):
    """Uploads a file to an S3 bucket."""
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    try:
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, key)
        return True
    except ClientError as e:
        return False


def check_file_exist(key):
    """Checks if a file exists in an S3 bucket."""
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME,
                      )
    try:
        s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True
    except ClientError:
        return False