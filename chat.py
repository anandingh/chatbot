import requests
import time
import random

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

# Main bot loop
def run_chat_bot():
    print("Available models:")
    for key, model in models.items():
        print(f"{key}. {model}")
    
    # Ask the user to choose a model
    model_choice = input("Please select a model (1-5): ")
    if model_choice not in models:
        print("Invalid choice. Exiting.")
        return
    
    selected_model = models[model_choice]
    print(f"Selected model: {selected_model}")
    
    # Ask for 100 questions
    print("Please enter 100 questions (each ending with a '?'):")
    questions = []
    for i in range(100):
        question = input(f"Enter question {i+1}: ")
        while not question.endswith('?'):
            print(f"Question {i+1} must end with a '?'. Please try again.")
            question = input(f"Enter question {i+1}: ")
        questions.append(question)
    
    # Verify we have 100 questions
    print(f"Total questions loaded: {len(questions)}")

    # Run through the questions and get answers
    print("\nStarting automated chat bot...")
    available_questions = questions.copy()
    
    for i in range(100):  # Fixed to 100 since we have exactly 100 questions
        if not available_questions:
            print("Ran out of questions unexpectedly!")
            break
        
        # Pick and remove a random question to avoid repetition
        question = random.choice(available_questions)
        available_questions.remove(question)
        
        # Send request and print results
        print(f"\nQuestion {i + 1}: {question}")
        answer = send_chat_request(question, model_choice)
        print(f"Answer: {answer}")
        
        # Random delay between 1-2 minutes (60-120 seconds)
        delay = random.uniform(60, 120)
        print(f"Waiting {delay:.1f} seconds before next question...")
        time.sleep(delay)
    
    print("\nCompleted 100 questions!")

# Run the bot
if __name__ == "__main__":
    run_chat_bot()
