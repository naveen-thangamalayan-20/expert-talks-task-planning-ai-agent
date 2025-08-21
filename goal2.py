import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:7b"

conversation_history = []


def call_llm_message(prompt_messages):
    response = requests.post(OLLAMA_API_URL,
                             json={"model": OLLAMA_MODEL, "messages": prompt_messages, "stream": False,
                                   "format": "json"},
                             timeout=120)  # Increased timeout for local LLM
    response.raise_for_status()  # Raise an exception for HTTP errors
    llm_output = response.json()['message']['content']
    return llm_output


def run_agent_loop():
    while True:
        user_input = input("You:").strip()
        if user_input == "quit":
            break
        elif not user_input:
            continue
        conversation_history.append(({"role": "user", "content": user_input}))
        result = call_llm_message(conversation_history)
        conversation_history.append({"role": "assistant", "content": result})
        print(result)


run_agent_loop()
