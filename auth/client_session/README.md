# session_auth.py

this library augments the boto3 client function by checking if it's
running on an EC2 instance or ECS container and if so, establishes the
client connection without local credentials, assuming there
is a instance role or task execution role assigned.
if there's no indication that you're running on an AWS instance/
container, then we assume you're running locally & have credentials
in environment variables.

The whole point of this library is to let folks test locally with
credentials in evn vars, but then not have those env vars on a running
container & instead relying on IAM roles for permissions.

local credential environment variables should be named according to
AWS documenation:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION

Usage:

```
pip install dist/clientsessionauth-0.1.0-py3-none-any.whl
from clientsessionauth import session_auth
```

call the **session_auth.get_client** function and pass it a service name that you
want to work with, e.g. ecs, ses, s3, etc..

```
client = session_auth.get_client('sts')
```

A boto3 client connection is returned.

## Contribute

```
python -m pip install venv
python -m venv venv
source venv/bin/activate
pip install --upgrade setuptools wheel twine
```

- modify code
- modify setup.py if needed

```
python setup.py bdist_wheel
```

## Usage

`pip install dist/clientsessionauth`

```
import boto3
from clientsessionauth import session_auth

client = session_auth.get_client('ecs')
...
```
