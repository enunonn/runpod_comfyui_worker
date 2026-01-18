# Runpod ComfyUI Worker

This repository contains the Dockerfile for a custom ComfyUI worker on Runpod.

## Setup

1. **Build the image**:
   ```bash
   docker build -t my-comfy-worker --build-arg CIVITAI_API_TOKEN=your_token_here .
   ```
2. **Push to registry**:
   ```bash
   docker tag my-comfy-worker myusername/my-comfy-worker:latest
   docker push myusername/my-comfy-worker:latest
   ```
3. **Run on Runpod**:
   - Create a new Template on Runpod.
   - Use the image name you pushed (e.g., `myusername/my-comfy-worker:latest`).
   - Create a Serverless Endpoint using this template.
