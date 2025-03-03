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

    # Print and log output in real-time
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)  # Print to console
        sys.stdout.flush()  # Ensure immediate output

    process.stdout.close()
    process.wait()  # Wait for the process to complete
    return process.returncode  # Return the exit status of the command


def train(job):
    config = job["input"]

    # Validate config against AppConfig
    try:
        config = AppConfig.model_validate(config)
    except Exception as e:
        return {"error": str(e)}

    username = config.username
    lora_name = config.lora_name
    class_tokens = config.class_tokens
    sample_prompt = config.sample_prompt if config.sample_prompt else class_tokens

    model_name = "flux-dev"

    save_dataset(config.dataset_config, username,
                 lora_name, class_tokens, space_client)
    print("Downloading models...")
    download_models(model_name)
    print("Generating training command...")
    write_command(username, lora_name)
    print("Writing sample prompt...")
    generate_sample_prompt(username, lora_name, sample_prompt)
    print("Training started...")

    # Run training script and wait until it completes
    exit_code = run_command(
        f"bash /app/scripts/outputs/{username}/{lora_name}/train.sh")

    if exit_code == 0:
        return {"message": "Training completed successfully"}
    else:
        return {"error": f"Training failed with exit code {exit_code}"}

if __name__ == "__main__":
    runpod.serverless.start( {"handler": train} )
    # uvicorn.run(app, port=8001, host="0.0.0.0")
