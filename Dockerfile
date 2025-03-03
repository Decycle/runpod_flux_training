# Base image with CUDA 12.4
FROM nvidia/cuda:12.4.1-base-ubuntu22.04

# Install pip if not already installed
RUN apt-get update -y && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    ffmpeg libsm6 libxext6 \
    build-essential  # Install dependencies for building extensions

WORKDIR /app

# Get sd-scripts from kohya-ss and install them
RUN git clone -b sd3 https://github.com/kohya-ss/sd-scripts && \
    cd sd-scripts && \
    pip install --no-cache-dir -r ./requirements.txt

# Install main application dependencies
# COPY ./requirements.txt ./requirements.txt
# RUN pip install --no-cache-dir -r ./requirements.txt
COPY ./scripts/requirements.txt /app/scripts/requirements.txt
RUN pip install --no-cache-dir -r /app/scripts/requirements.txt

# Install Torch, Torchvision, and Torchaudio for CUDA 12.4
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Copy fluxgym application code
COPY ./scripts /app/scripts
WORKDIR /app/scripts

RUN pip uninstall triton -y

# Run fluxgym Python application
CMD ["python3", "api.py"]

# pause
# CMD ["tail", "-f", "/dev/null"]