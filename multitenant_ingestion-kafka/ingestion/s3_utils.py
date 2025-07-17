import boto3
from django.conf import settings
# s3_client = boto3.client('s3',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
s3_client = boto3.client('s3')
def upload_file_to_s3(file, tenant_id, filename):
    key = f'{tenant_id}/{filename}'
    s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, key)
    return key
def get_file_from_s3(key):
    return s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)['Body'].read()
def delete_file_from_s3(key):
    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
