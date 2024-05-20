import boto3

class S3:

    def __init__(self):
        self.s3 = boto3.client('s3')

    def upload_object(self, key, data, bucket_name):
        self.s3.put_object(Bucket=bucket_name, Key=key, Body=data)
