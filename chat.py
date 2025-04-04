import requests
import time
import random
import os

# API Configuration
URL = "https://api.hyperbolic.xyz/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaW5naGFuYW5kMzAyNzNAZ21haWwuY29tIn0.wsc9OccMPpTpsHTrqK3HNrfaOQGdaQjyf-XEiPN-rNg"
}

# Available models list
models = {
    "1": "deepseek-ai/DeepSeek-V3-0324",
    "2": "meta-llama/Llama-3.3-70B-Instruct",
    "3": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "4": "meta-llama/Llama-3.2-3B-Instruct",
    "5": "Qwen/Qwen2.5-72B-Instruct"
}

# Function to send API request based on the selected model
def send_chat_request(question, model_choice):
    model_name = models[model_choice]
    
    data = {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "model": model_name,
        "max_tokens": 15486,
        "temperature": 0.1,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(URL, headers=HEADERS, json=data)
        response.raise_for_status()
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

# Function to create the q.txt file with two sample questions if it doesn't exist
def create_qtxt_file(file_path="q.txt"):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('"What is the impact of global warming?", "How does urbanization affect climate?"')
        print(f"The 'q.txt' file has been created at {file_path} with sample questions.")
        print("Please add your questions in the same format (each question enclosed in quotes and separated by commas).")
        print("After adding your questions, save the file and restart the bot.")
    else:
        print(f"Found 'q.txt' file at {file_path}. Now, reading the questions...")

# Function to read questions from the file
def read_questions_from_file(file_path="q.txt"):
    with open(file_path, 'r') as file:
        questions_input = file.read()

    # Split questions by commas, strip out extra spaces and quotes
    questions = [q.strip().strip('"') for q in questions_input.split(',') if q.strip()]

    # Filter out questions that don't end with a "?"
    valid_questions = [q for q in questions if q.endswith('?')]

    return valid_questions

# Main bot loop
def run_chat_bot():
    # Step 1: Create the q.txt file (if it doesn't exist) and instruct the user to add questions manually.
    create_qtxt_file()

    # Wait for 30 seconds to give the user time to add questions
    print("\nWaiting for 30 seconds to allow you to add questions...")
    time.sleep(30)

    # Step 2: After the wait, check if the file exists and read the questions
    print("\nReading questions from the q.txt file...")
    questions = read_questions_from_file()
    
    # If no valid questions are found, notify the user
    if len(questions) == 0:
        print("No valid questions found in the file. Please ensure each question ends with a '?'.")
        return

    # Ask the user to choose a model
    print("\nAvailable models:")
    for key, model in models.items():
        print(f"{key}. {model}")
    
    model_choice = input("Please select a model (1-5): ")
    if model_choice not in models:
        print("Invalid choice. Exiting.")
        return
    
    selected_model = models[model_choice]
    print(f"Selected model: {selected_model}")
    
    # Run through the questions and get answers
    print("\nStarting automated chat bot...")
    available_questions = questions.copy()

    for i, question in enumerate(available_questions):  # Use the available questions
        # Send request and print results
        print(f"\nQuestion {i + 1}: {question}")
        answer = send_chat_request(question, model_choice)
        print(f"Answer: {answer}")
        
        # Random delay between 1-2 minutes (60-120 seconds)
        delay = random.uniform(60, 120)
        print(f"Waiting {delay:.1f} seconds before next question...")
        time.sleep(delay)
    
    print("\nCompleted all questions!")

# Run the bot
if __name__ == "__main__":
    run_chat_bot()
