import openai
from openai import OpenAI
import requests
import time
import os
import unreal

# API Keys
BLOCKADE_LABS_API_KEY = os.getenv("BLOCKADE_LABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Setup
openai.api_key = OPENAI_API_KEY

# Initialize the client
client = OpenAI(api_key=OPENAI_API_KEY)

def refine_prompt(base_prompt):
    """Refine a user-provided prompt into a detailed description."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", 
                 "content": "You are a creative assistant specializing in improving 3D skybox descriptions. "
                        "Make the prompt more vivid, descriptive, and detailed while maintaining relevance "
                        "to the original theme. Ensure the response is concise and within 500 characters."},
                {"role": "user", "content": f"Refine this description for a 3D skybox: {base_prompt}"}
            ]
        )
        refined_prompt = response.choices[0].message.content.strip()[:400]
        return refined_prompt
    except Exception as e:
        print(f"Error refining prompt: {e}")
        return base_prompt


def generate_skybox(prompt, style_id):
    """Send a request to generate a skybox."""
    url = "https://backend.blockadelabs.com/api/v1/skybox"
    headers = {"x-api-key": BLOCKADE_LABS_API_KEY, "Content-Type": "application/json"}
    payload = {"prompt": prompt, "skybox_style_id": style_id}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(f"Skybox generation request submitted: {data}")
        return data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_generation_status(generation_id):
    """Check the status of a skybox generation."""
    url = f"https://backend.blockadelabs.com/api/v1/imagine/requests/{generation_id}"
    headers = {"x-api-key": BLOCKADE_LABS_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #print(f"Response Data: {data}")
        return data.get("request")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def download_skybox(file_url, save_path):
    """Download the HDRI skybox file."""
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Skybox saved to {save_path}")
    else:
        print(f"Failed to download skybox: {response.status_code}")

def import_hdri_to_ue5(hdri_path, destination_path):
    """Import HDRI files into Unreal Engine 5."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    import_task = unreal.AssetImportTask()
    import_task.set_editor_property('filename', hdri_path)
    import_task.set_editor_property('destination_path', destination_path)
    import_task.set_editor_property('replace_existing', True)
    import_task.set_editor_property('save', True)
    import_task.set_editor_property('automated', True)

    asset_tools.import_asset_tasks([import_task])
    print(f"Imported HDRI from {hdri_path} to {destination_path}")

# Main Workflow
base_prompt = "A futuristic utopian cityscape "
refined_prompt = refine_prompt(base_prompt)
response = generate_skybox(refined_prompt, 35)

if response:
    generation_id = response.get("id")
    print(f"Generation ID: {generation_id}")

    while True:
        status_response = get_generation_status(generation_id)
        if status_response and "status" in status_response:
            generation_status = status_response["status"]
            print(f"Status: {generation_status}\n")

            if generation_status in ["complete", "error", "abort"]:
                if generation_status == "complete":
                    skybox_url = status_response.get("file_url")
                    viewer_url = f"https://skybox.blockadelabs.com/{status_response['obfuscated_id']}"
                    print(f"Base Prompt: {base_prompt}")
                    print(f"Refined Prompt: {refined_prompt}")
                    print(f"Skybox URL: {skybox_url}")
                    print(f"360 View URL: {viewer_url}\n")

                    # Save HDRI locally
                    save_directory = "output"
                    os.makedirs(save_directory, exist_ok=True)
                    save_path = os.path.join(save_directory, f"skybox_{generation_id}.hdr")

                    download_skybox(skybox_url, save_path)

                    # Import into Unreal Engine 5
                    destination_content_path = "/Game/HDRIs"
                    import_hdri_to_ue5(save_path, destination_content_path)
                break
        else:
            print("Status key not found in response. Retrying...")
        time.sleep(5)
