FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

# Install common tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget curl vim tmux build-essential && \
    rm -rf /var/lib/apt/lists/*

# (Optional) Install extra Python packages
RUN pip install --no-cache-dir nnunetv2

# Set nnUNet v2 environment variables
ENV nnUNet_raw=/workspace/nnUNet_raw
ENV nnUNet_preprocessed=/workspace/nnUNet_preprocessed
ENV nnUNet_results=/workspace/nnUNet_results

WORKDIR /workspace
