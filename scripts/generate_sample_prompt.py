from pathlib import Path
import os

def generate_sample_prompt(username, lora_name, sample_prompt):
    # sample_prompt
    filename = Path("/app/scripts/outputs") / username / lora_name / "sample_prompts.txt"
    os.makedirs(filename.parent, exist_ok=True)
    with open(filename, "w") as f:
        f.write(sample_prompt)