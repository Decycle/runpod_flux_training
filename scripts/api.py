from pydantic import BaseModel, Field
# from fastapi import FastAPI
import hashlib
import boto3
import os
import dotenv
# import uvicorn
from pathlib import Path
import subprocess

import runpod
from runpod.serverless.utils.rp_validator import validate

import sys
sys.path.append("/app")

from scripts.utils.space import init_space
from schema.app_config import AppConfig
from scripts.save_dataset import save_dataset
from scripts.download_model import download_models
from scripts.generate_sample_prompt import generate_sample_prompt
from scripts.generate_command import write_command
dotenv.load_dotenv()

# app = FastAPI()
space_client = init_space()

download_models("flux-dev")

def run_command(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,  # Ensures text mode (instead of bytes)
        bufsize=1  # Line buffering
    )

    # Print and log output in real time
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)  # Print to console
        sys.stdout.flush()  # Ensure immediate output

    process.stdout.close()
    process.wait()


def train(job):
    job_input = job["input"]
    validated_input = validate(job_input, AppConfig)

    if "errors" in validated_input:
        return {"error": validated_input["errors"]}
    config = validated_input["validated_input"]

    username = config.username
    lora_name = config.lora_name
    class_tokens = config.class_tokens
    sample_prompt = config.sample_prompt if config.sample_prompt else class_tokens

    model_name = "flux-dev"

    save_dataset(config.dataset_config, username, lora_name, class_tokens, space_client)
    print("Downloading models...")
    download_models(model_name)
    print("Generate training command...")
    write_command(username, lora_name)
    print("Write down sample prompt...")
    generate_sample_prompt(username, lora_name, sample_prompt)
    print("Training started")

    run_command(f"bash /app/scripts/outputs/{username}/{lora_name}/train.sh")

    return {"message": "Training started"}

if __name__ == "__main__":
    runpod.serverless.start( {"handler": train} )
    # uvicorn.run(app, port=8001, host="0.0.0.0")
