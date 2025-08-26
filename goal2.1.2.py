import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:7b"


def call_llm(prompt_messages):
    response = requests.post(OLLAMA_API_URL,
                             json={"model": OLLAMA_MODEL, "messages": prompt_messages, "stream": False,
                                   },
                             timeout=120)
    response.raise_for_status()
    llm_output = response.json()['message']['content']
    return llm_output

conversation_history = []

def run():
    conversation_history.append(({"role": "system", "content": "Assume you are a poet and provide answer to user as haiku"}))
    conversation_history.append(({"role": "user", "content": "Explain the about india ?"}))
    print(call_llm(conversation_history))

run()
