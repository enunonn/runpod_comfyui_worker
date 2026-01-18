#!/bin/bash
set -e

# Start ComfyUI in background
echo "Starting ComfyUI..."
python /ComfyUI/main.py --listen --port 8188 &

# Wait for ComfyUI to be ready
echo "Waiting for ComfyUI to be ready..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8188/ > /dev/null; then
        echo "ComfyUI is ready!"
        break
    fi
    sleep 2
done

# Run the handler
echo "Starting RunPod Handler..."
python /handler.py
