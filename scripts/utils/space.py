import os
import boto3

def init_space():
    RUNPOD_IMG_READ_SECRET = os.getenv("RUNPOD_IMG_READ_SECRET")
    RUNPOD_IMG_READ_ACCESS = os.getenv("RUNPOD_IMG_READ_ACCESS")
    SPACE_URL = "https://fluxtrain.nyc3.digitaloceanspaces.com/"


    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url=SPACE_URL,
                            region_name='nyc3',
                            aws_access_key_id=RUNPOD_IMG_READ_ACCESS,
                            aws_secret_access_key=RUNPOD_IMG_READ_SECRET
                            )
    return client