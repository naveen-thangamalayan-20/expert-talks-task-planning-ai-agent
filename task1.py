# --- Configuration ---
import json

import requests

# OLLAMA_API_BASE_URL = "http://localhost:11434/api/chat"
OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_MODEL = "qwen2.5:7b" # Ensure you have 'qwen' model pulled in Ollama

def call_llm(prompt):
    url = OLLAMA_API_BASE_URL + "/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    response = requests.post(url, json=payload)
    response_json = response.json()
    print(response_json)
    # print(json.dumps(response_json, indent=2))

call_llm("Who are you ?")



