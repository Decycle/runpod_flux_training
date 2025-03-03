#! /bin/bash

# build command
docker build -t runpod_flux_finetune:0.0.1 .
# run command
docker run -it --gpus all -p 8001:8001 --name runpod_flux_finetune_v2 runpod_flux_finetune:0.0.2
