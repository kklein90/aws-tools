import boto3
from botocore.exceptions import ClientError
import os

'''
Generate a presigned URL to share an S3 object
Run:
python -m pip install virtualenv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Export your AWS credentials in your shell:
export TS_AWS_ACCESS_KEY_ID="provided by kris"
export TS_AWS_SECRET_ACCESS_KEY="provided by kris"

python generate_presigned_url.py

copy/paste the URL into your browser to download the file
'''

def create_presigned_url(bucket_name, object_name, expiration=3600):
    ACCESS_KEY = os.getenv('TS_AWS_ACCESS_KEY_ID')
    SECRET_KEY = os.getenv('TS_AWS_SECRET_ACCESS_KEY')
    s3_client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(f"Couldn't get a presigned URL: {e}")
        return None
    return response

if __name__ == "__main__":
	presigned_url = create_presigned_url("typeset-stg-public", "cappy.webp", expiration=3600)
	print(presigned_url)
