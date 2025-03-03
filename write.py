import hashlib
import requests
import streamlit as st
import boto3
import os
import dotenv
import slugify

dotenv.load_dotenv()


USER_UPLOAD_IMG_SECRET = os.getenv("USER_UPLOAD_IMG_SECRET")
USER_UPLOAD_IMG_ACCESS = os.getenv("USER_UPLOAD_IMG_ACCESS")
SPACE_URL = "https://fluxtrain.nyc3.digitaloceanspaces.com/"


@st.cache_resource
def connect_to_space():
    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url=SPACE_URL,
                            region_name='nyc3',
                            aws_access_key_id=USER_UPLOAD_IMG_ACCESS,
                            aws_secret_access_key=USER_UPLOAD_IMG_SECRET
                            )
    return client

client = connect_to_space()
hasher = hashlib.md5()


@st.cache_data
def upload_img(img, user_name, client=client, file_type="png"):
    hasher.update(img.getvalue())  # Update hash with image data
    # Use computed hash for filename
    hash = hasher.hexdigest()
    file_name = f"{user_name}/{hash}.{file_type}"
    img.seek(0)  # Reset stream position if you need to read the file again
    response = client.put_object(
        Bucket='images',
        Key=file_name,
        Body=img,
        ContentType=f'image/{file_type}',
        ACL='private'
    )
    return hash

@st.cache_data
def upload_images(upload_files, user_name):
    hash_ids = []
    for uploaded_file in upload_files:
        hash = upload_img(uploaded_file, user_name)
        hash_ids.append(hash)
    return hash_ids

st.write("Choose your images to upload")
upload_files = st.file_uploader("Choose images...", type="png", accept_multiple_files=True)

hash_ids = []

username = st.text_input("Username", "decycle")
lora_name = st.text_input("Lora name", "chinese-maid")
if st.button("Upload"):
    hash_ids = upload_images(upload_files, username)
    st.write(hash_ids)

print(len(hash_ids), len(upload_files))
if len(hash_ids) != 0 and len(hash_ids) == len(upload_files):
    class_tokens = "p1rs0n"

    images = [{"filename": f"{hash}.png"} for hash in hash_ids]
    datasetConfig = {
        "images": images,
        "auto_generate_captions": False,
        "resolution": 512
    }

    payload = {
        "images": images,
        "dataset_config": datasetConfig,
        "username": username,
        "lora_name": lora_name,
        "class_tokens": class_tokens,
        "sample_prompt": f"A beautiful image of {class_tokens}",
    }
    response = requests.post(
        "http://localhost:8002/train", json=payload)
    if response.status_code == 200:
        st.success("Saved!")
    else:
        st.error("Failed to save")
        st.write(response.json())