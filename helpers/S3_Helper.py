import boto3

class S3_Helper:
    def __init__(self):
        self.client = boto3.client('s3')

    def upload_file(self, bucket_name, file_name):
        self.client.upload_file(file_name, bucket_name, file_name)

    def list_objects(self, bucket_name):
        response = self.client.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            print(obj['Key'])

    def download_object(self, bucket_name, key):
        response = self.client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read().decode('utf-8')
