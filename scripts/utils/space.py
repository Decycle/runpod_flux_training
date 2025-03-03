import os
import boto3

def init_space():
    SPACE_RUNPOD_IMG_READ_SECRET = os.getenv("SPACE_RUNPOD_IMG_READ_SECRET")
    SPACE_RUNPOD_IMG_READ_ACCESS = os.getenv("SPACE_RUNPOD_IMG_READ_ACCESS")
    SPACE_URL = "https://fluxtrain.nyc3.digitaloceanspaces.com/"


    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url=SPACE_URL,
                            region_name='nyc3',
                            aws_access_key_id=SPACE_RUNPOD_IMG_READ_ACCESS,
                            aws_secret_access_key=SPACE_RUNPOD_IMG_READ_SECRET
                            )
    return client