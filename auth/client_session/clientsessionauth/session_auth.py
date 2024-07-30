import boto3
import requests
import os

'''
determine if we're running on an AWS resource (EC2 instance)
'''

def am_i_on_aws():
    metadata_url = "http://169.254.169.254/latest/api/token"
    http_headers = { 'X-aws-ec2-metadata-token-ttl-seconds': "600", "content-type": "application/json"}
    try:
        token = requests.put(metadata_url, headers=http_headers, timeout=1, allow_redirects=True)
    except requests.exceptions.ConnectTimeout as e:
        return 1
    return token.text

def local_client(service):
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_region = os.environ['AWS_DEFAULT_REGION']

    client = boto3.client(
        service,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    return client

def aws_client(service):
    client = boto3.client(service)
    return client

def get_client(service):
    r = am_i_on_aws

    if r == 1:
        client = local_client(service)
        return client
    else:
        client = aws_client(service)
        return client


if __name__ == "__main__":
    print("don't run directly")