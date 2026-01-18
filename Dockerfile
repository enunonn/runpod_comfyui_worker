FROM runpod/worker-comfyui:5.7.1-base

ARG CIVITAI_API_TOKEN

RUN comfy-node-install comfyui-kjnodes comfyui-ic-light
RUN comfy-node-install ComfyUI-WanVideoWrapper rgthree-comfy ComfyUI-Easy-Use ComfyUI-VideoHelperSuite
RUN comfy-node-install was-node-suite-comfyui crt-nodes comfyui-notifications

# Download Models (Baking into image)
RUN comfy model download --url "https://civitai.com/api/download/models/2512333?type=Model&format=SafeTensor&size=full&fp=fp8&token=${CIVITAI_API_TOKEN}" --relative-path models/checkpoints --filename DaSiWa_WAN_2.2_I2V_14B_TastySin_v8_Low.safetensors
RUN comfy model download --url "https://civitai.com/api/download/models/2260110?type=Model&format=SafeTensor&size=pruned&fp=fp8&token=${CIVITAI_API_TOKEN}" --relative-path models/checkpoints --filename Smooth_Mix_Wan_2.2_14B_High.safetensors
RUN comfy model download --url "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Stable-Video-Infinity/v2.0/SVI_v2_PRO_Wan2.2-I2V-A14B_HIGH_lora_rank_128_fp16.safetensors?download=true" --relative-path models/loras --filename SVI_v2_PRO_Wan2.2-I2V-A14B_HIGH_lora_rank_128_fp16.safetensors
RUN comfy model download --url "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Stable-Video-Infinity/v2.0/SVI_v2_PRO_Wan2.2-I2V-A14B_LOW_lora_rank_128_fp16.safetensors?download=true" --relative-path models/loras --filename SVI_v2_PRO_Wan2.2-I2V-A14B_LOW_lora_rank_128_fp16.safetensors
RUN wget -q https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors -O /ComfyUI/models/clip_vision/clip_vision_h.safetensors
RUN wget -q https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors -O /ComfyUI/models/text_encoders/umt5-xxl-enc-bf16.safetensors
RUN wget -q https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors -O /ComfyUI/models/vae/Wan2_1_VAE_bf16.safetensors

# Copy handler and entrypoint
COPY handler.py /handler.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set Entrypoint
CMD ["/entrypoint.sh"]
