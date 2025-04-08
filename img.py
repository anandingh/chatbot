import requests
import time
import random
import os

# Function to get the API key from the user
def get_api_key():
    api_key = input("Please enter your API key: ")
    return api_key

# API Configuration (API key will be provided by the user)
URL = "https://api.hyperbolic.xyz/v1/image/generation"
def get_headers(api_key):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

# Available models list for image generation
models = {
    "1": "FLUX.1-dev",
    "2": "SDXL1.0-base",
    "3": "SD1.5",
    "4": "SSD",
    "5": "SD2",
    "6": "SDXL-turbo"
}

# Function to send API request to generate an image based on the selected model
def send_image_request(prompt, model_choice, headers):
    model_name = models[model_choice]
    
    data = {
        "model_name": model_name,
        "prompt": prompt,
        "enable_refiner": "false",
        "negative_prompt": "",
        "strength": "0.8",
        "steps": "30",
        "cfg_scale": "5",
        "resolution": "1024x1024",
        "backend": "auto"
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if 'image_url' in result:
            return f"Image successfully generated! Link: {result['image_url']}"
        else:
            return "Failed to generate image."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to create the q.txt file with two sample prompts if it doesn't exist
def create_qtxt_file(file_path="q.txt"):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('"A beautiful sunset over a calm ocean", "A futuristic city at night"')
        print(f"The 'q.txt' file has been created at {file_path} with sample prompts.")
        print("Please add your prompts in the same format (each prompt enclosed in quotes and separated by commas).")
        print("After adding your prompts, save the file and restart the bot.")
    else:
        print(f"Found 'q.txt' file at {file_path}. Now, reading the prompts...")

# Function to read prompts from the file
def read_prompts_from_file(file_path="q.txt"):
    with open(file_path, 'r') as file:
        prompts_input = file.read()

    # Split prompts by commas, strip out extra spaces and quotes
    prompts = [p.strip().strip('"') for p in prompts_input.split(',') if p.strip()]

    return prompts

# Main bot loop
def run_image_bot():
    # Step 1: Get the API key from the user
    api_key = get_api_key()
    headers = get_headers(api_key)

    # Step 2: Create the q.txt file (if it doesn't exist) and instruct the user to add prompts manually.
    create_qtxt_file()

    # Wait for 10 seconds to give the user time to add prompts
    print("\nWaiting for 10 seconds to allow you to add prompts...")
    time.sleep(10)

    # Step 3: After the wait, check if the file exists and read the prompts
    print("\nReading prompts from the q.txt file...")
    prompts = read_prompts_from_file()
    
    # If no prompts are found, notify the user
    if len(prompts) == 0:
        print("No prompts found in the file. Please add your prompts and restart the bot.")
        return

    # Ask the user to choose a model
    print("\nAvailable models for image generation:")
    for key, model in models.items():
        print(f"{key}. {model}")
    
    model_choice = input("Please select a model (1-6): ")
    if model_choice not in models:
        print("Invalid choice. Exiting.")
        return
    
    selected_model = models[model_choice]
    print(f"Selected model: {selected_model}")
    
    # Run through the prompts and generate images
    print("\nStarting image generation bot...")
    available_prompts = prompts.copy()

    for i, prompt in enumerate(available_prompts):  # Use the available prompts
        # Send request and print results
        print(f"\nPrompt {i + 1}: {prompt}")
        result = send_image_request(prompt, model_choice, headers)
        print(result)
        
        # Random delay between 1-2 minutes (60-120 seconds)
        delay = random.uniform(60, 120)
        print(f"Waiting {delay:.1f} seconds before next prompt...")
        time.sleep(delay)
    
    print("\nCompleted all prompts!")

# Run the bot
if __name__ == "__main__":
    run_image_bot()
