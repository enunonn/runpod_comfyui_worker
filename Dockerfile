FROM runpod/worker-comfyui:5.7.1-base

ARG CIVITAI_API_TOKEN

RUN comfy-node-install comfyui-kjnodes comfyui-ic-light
RUN comfy-node-install ComfyUI-WanVideoWrapper rgthree-comfy ComfyUI-Easy-Use ComfyUI-VideoHelperSuite
RUN comfy-node-install was-node-suite-comfyui crt-nodes comfyui-notifications

# Copy download script for manual execution or runtime
COPY download_models.py /root/download_models.py
