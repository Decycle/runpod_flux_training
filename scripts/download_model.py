import os
from huggingface_hub import hf_hub_download

models= {
    "flux-dev": {
        'file': 'flux1-dev.sft',
        'repo': 'cocktailpeanut/xulf-dev'
    },
}

def download_models(base_model: str):
    model = models[base_model]
    model_file = model["file"]
    repo = model["repo"]

    # download unet
    if base_model == "flux-dev" or base_model == "flux-schnell":
        unet_folder = "models/unet"
    else:
        unet_folder = f"models/unet/{repo}"
    unet_path = os.path.join(unet_folder, model_file)
    if not os.path.exists(unet_path):
        os.makedirs(unet_folder, exist_ok=True)
        print(f"download {base_model}")
        hf_hub_download(repo_id=repo, local_dir=unet_folder,
                        filename=model_file)

    # download vae
    vae_folder = "models/vae"
    vae_path = os.path.join(vae_folder, "ae.sft")
    if not os.path.exists(vae_path):
        os.makedirs(vae_folder, exist_ok=True)
        hf_hub_download(repo_id="cocktailpeanut/xulf-dev",
                        local_dir=vae_folder, filename="ae.sft")

    # download clip
    clip_folder = "models/clip"
    clip_l_path = os.path.join(clip_folder, "clip_l.safetensors")
    if not os.path.exists(clip_l_path):
        os.makedirs(clip_folder, exist_ok=True)
        print(f"download clip_l.safetensors")
        hf_hub_download(repo_id="comfyanonymous/flux_text_encoders",
                        local_dir=clip_folder, filename="clip_l.safetensors")

    # download t5xxl
    t5xxl_path = os.path.join(clip_folder, "t5xxl_fp16.safetensors")
    if not os.path.exists(t5xxl_path):
        print(f"download t5xxl_fp16.safetensors")
        hf_hub_download(repo_id="comfyanonymous/flux_text_encoders",
                        local_dir=clip_folder, filename="t5xxl_fp16.safetensors")
