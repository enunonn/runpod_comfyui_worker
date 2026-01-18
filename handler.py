import runpod
import json
import time
import websocket
import uuid
import urllib.request
import urllib.parse
from runpod.serverless.utils import rp_upload

SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()

def handler(job):
    job_input = job["input"]
    workflow = job_input.get("workflow")
    
    if not workflow:
        return {"error": "No workflow provided"}

    # Connect to WebSocket
    ws = websocket.WebSocket()
    ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")

    try:
        # Submit prompt
        prompt_response = queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']
        
        # Wait for completion
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break # Execution finished

        # Retrieve results
        history = get_history(prompt_id)[prompt_id]
        outputs = []
        
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    # Get image data
                    img_data = get_image(image['filename'], image['subfolder'], image['type'])
                    
                    # Upload to Runpod Storage (S3) if configured, or return base64
                    # Here we assume returning base64 for simplicity, or upload URL if buckets are set
                    # For this example, let's just return the filename indicating success
                    outputs.append({
                        "filename": image['filename'],
                        "subfolder": image['subfolder'],
                        "type": image['type']
                    })
                    
        return {"status": "success", "outputs": outputs}

    except Exception as e:
        return {"error": str(e)}
    finally:
        ws.close()

runpod.serverless.start({"handler": handler})
