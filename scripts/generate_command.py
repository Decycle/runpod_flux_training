import shlex
from pathlib import Path


def generate_train_command(pretrained_model_name_or_path, clip_l, t5xxl, ae, sample_prompts, sample_every_n_steps, seed, dataset_config, output_dir, output_name):
    base_command = "accelerate launch --mixed_precision bf16 --num_cpu_threads_per_process 1 "
    args = {
        "pretrained_model_name_or_path": pretrained_model_name_or_path,
        "clip_l": clip_l,
        "t5xxl": t5xxl,
        "ae": ae,
        "mixed_precision": "bf16",
        "cache_latents_to_disk": True,
        "save_model_as": "safetensors",
        "sdpa": True,
        "persistent_data_loader_workers": True,
        "max_data_loader_n_workers": 2,
        "seed": seed,
        "gradient_checkpointing": True,
        "save_precision": "bf16",
        "network_module": "networks.lora_flux",
        "network_dim": 4,
        "optimizer_type": "adamw8bit",
        "sample_prompts": sample_prompts,
        "sample_every_n_steps": sample_every_n_steps,
        "learning_rate": "8e-4",
        "cache_text_encoder_outputs": True,
        "cache_text_encoder_outputs_to_disk": True,
        "fp8_base": True,
        "highvram": True,
        "max_train_epochs": 16,
        "save_every_n_epochs": 4,
        "dataset_config": dataset_config,
        "output_dir": output_dir,
        "output_name": output_name,
        "timestep_sampling": "shift",
        "discrete_flow_shift": 3.1582,
        "model_prediction_type": "raw",
        "guidance_scale": 1,
        "loss_type": "l2",
        "log_config": True,
        "log_with": "wandb",
        "wandb_run_name": "flux_test",
    }

    cmd_parts = [base_command, "/app/sd-scripts/flux_train_network.py"]

    for key, value in args.items():
        if isinstance(value, bool):
            if value:
                cmd_parts.append(f"--{key}")
        else:
            cmd_parts.append(f"--{key}")
            cmd_parts.append(shlex.quote(str(value)))

    return " ".join(cmd_parts)

def write_command(username, lora_name):
    script_dir = Path("/app/scripts")
    model_dir = script_dir / "models"
    output_dir = script_dir / "outputs" / username / lora_name


    cmd = generate_train_command(
        pretrained_model_name_or_path=(model_dir / "unet" / "flux1-dev.sft").as_posix(),
        clip_l=(model_dir / "clip" / "clip_l.safetensors").as_posix(),
        t5xxl=(model_dir / "clip" / "t5xxl_fp16.safetensors").as_posix(),
        ae=(model_dir / "vae" / "ae.sft").as_posix(),
        sample_prompts=(output_dir / "sample_prompts.txt").as_posix(),
        sample_every_n_steps="500",
        seed=42,
        dataset_config=(output_dir / "dataset.toml").as_posix(),
        output_dir=output_dir.as_posix(),
        output_name=lora_name
    )

    with open(output_dir / "train.sh", "w") as f:
        f.write(cmd)
