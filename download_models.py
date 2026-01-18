import os
import subprocess

# Civitai Token (환경변수에서 로드)
CIVITAI_TOKEN = os.environ.get("CIVITAI_API_TOKEN", "")

# 모델 다운로드 목록 설정
# (URL, 저장경로, 파일명)
models = [
    (f"https://civitai.com/api/download/models/2512333?type=Model&format=SafeTensor&size=full&fp=fp8&token={CIVITAI_TOKEN}", "models/checkpoints", "DaSiWa_WAN_2.2_I2V_14B_TastySin_v8_Low.safetensors"),
    (f"https://civitai.com/api/download/models/2260110?type=Model&format=SafeTensor&size=pruned&fp=fp8&token={CIVITAI_TOKEN}", "models/checkpoints", "Smooth_Mix_Wan_2.2_14B_High.safetensors"),
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Stable-Video-Infinity/v2.0/SVI_v2_PRO_Wan2.2-I2V-A14B_HIGH_lora_rank_128_fp16.safetensors?download=true", "models/loras", "SVI_v2_PRO_Wan2.2-I2V-A14B_HIGH_lora_rank_128_fp16.safetensors"),
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Stable-Video-Infinity/v2.0/SVI_v2_PRO_Wan2.2-I2V-A14B_LOW_lora_rank_128_fp16.safetensors?download=true", "models/loras", "SVI_v2_PRO_Wan2.2-I2V-A14B_LOW_lora_rank_128_fp16.safetensors"),
    ("https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors", "models/clip_vision", "clip_vision_h.safetensors"),
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors", "models/text_encoders", "umt5-xxl-enc-bf16.safetensors"),
    ("https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors", "models/vae", "Wan2_1_VAE_bf16.safetensors"),
]

def download_model(url, path, filename):
    full_path = f"/ComfyUI/{path}/{filename}"
    dir_path = os.path.dirname(full_path)
    
    if os.path.exists(full_path):
        print(f"✅ Already exists: {filename}")
        return

    print(f"⬇️ Downloading: {filename}...")
    os.makedirs(dir_path, exist_ok=True)
    
    # wget 사용 (SafeToAutoRun 고려하여 실제 커맨드는 문자열로 작성하지만 여기선 python subprocess 사용)
    try:
        subprocess.run(["wget", "-q", url, "-O", full_path], check=True)
        print(f"✅ Downloaded: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    if not CIVITAI_TOKEN:
        print("⚠️ Warning: CIVITAI_API_TOKEN environment variable is not set. Civitai downloads may fail.")
    
    print("🚀 Starting model downloads to /ComfyUI/...")
    for url, path, filename in models:
        download_model(url, path, filename)
    print("🎉 All downloads checked/completed.")
