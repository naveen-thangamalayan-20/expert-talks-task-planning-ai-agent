import requests

OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_MODEL = "qwen2.5:7b"

conversation_history = []


def call_llm(prompt):
    url = OLLAMA_API_BASE_URL + "/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    response_json = response.json()
    return response_json["response"]


def run_agent_loop():
    while True:
        user_input = input("You:").strip()
        if user_input == "quit":
            break
        elif not user_input:
            continue
        result = call_llm(user_input)
        print(result)


run_agent_loop()
