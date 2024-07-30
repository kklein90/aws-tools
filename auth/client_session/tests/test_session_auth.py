import boto3
import aksessionauth
from aksessionauth import session_auth

client = session_auth.get_client('sts')

response = client.get_caller_identity()
print(response)