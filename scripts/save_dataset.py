from schema.dataset_config import DatasetConfig, ImageData
import hashlib
import boto3
import os
import dotenv
from pathlib import Path
import toml

hasher = hashlib.md5()

def download_img(img_path, user_name, client):
    response = client.get_object(
        Bucket='images',
        Key=f"{user_name}/{img_path}"
    )
    return response['Body']

def save_img(imageData: ImageData, user_name, lora_name, client):
    img = download_img(imageData.filename, user_name, client)
    img_path = Path(f"images/{user_name}/{lora_name}/{imageData.filename}")
    img_path.parent.mkdir(parents=True, exist_ok=True)
    with open(img_path, "wb") as f:
        f.write(img.read())

    caption_path = img_path.with_suffix(".txt")
    with open(caption_path, "w") as f:
        f.write(imageData.caption)


def write_basic_dataset_config(resolution, image_dir, class_tokens, file_path):
    config = {
        "general": {
            "shuffle_caption": False,
            "caption_extension": ".txt",
            "keep_tokens": 1
        },
        "datasets": [
            {
                "resolution": resolution,
                "batch_size": 1,
                "keep_tokens": 1,
                "subsets": [
                    {
                        "image_dir": image_dir,
                        "class_tokens": class_tokens,
                        "num_repeats": 10
                    }
                ]
            }
        ]
    }

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        toml.dump(config, f)


def save_dataset(data: DatasetConfig, username, lora_name, class_tokens, client):
    # TODO: scale resolutions
    if data.auto_generate_captions:
        # TODO: regenerate captions
        pass
    else:
        # defaults caption to class tokens
        for img in data.images:
            if img.caption is None:
                img.caption = class_tokens
    for img in data.images:
        save_img(img, username, lora_name, client)

    write_basic_dataset_config(
        data.resolution,
        f"images/{username}/{lora_name}",
        class_tokens,
        f"outputs/{username}/{lora_name}/dataset.toml"
    )