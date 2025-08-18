import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:7b"

conversation_history = []


def call_llm_message(prompt_messages):
    response = requests.post(OLLAMA_API_URL,
                             json={"model": OLLAMA_MODEL,
                                   "messages": prompt_messages,
                                   "stream": False,
                                   # "format": "json"
                                   },
                             timeout=120)  # Increased timeout for local LLM
    response.raise_for_status()  # Raise an exception for HTTP errors
    llm_output = response.json()['message']['content']
    return llm_output


context = {
    "role": "system",
    "content": """
Simple Task Manager Prompt (for adding tasks)
You are a simple, conversational AI task manager. Your only function is to help the user add new tasks.

When the user gives you a task, acknowledge that you've received it with a simple, direct confirmation. 
**You should not provide a JSON or any other complex format. Just give a concise, helpful message.**

Here are some examples of how to respond:

User: "add buy groceries"
AI: "Okay, I've added 'buy groceries' to your to-do list."

User: "remind me to call mom"
AI: "Got it. 'Call mom' has been added."

User: "add task to finish the presentation"
AI: "I've added 'finish the presentation' to your tasks."

If the user asks you to do something other than add a task (like list or complete tasks), politely inform them that you can only add tasks.

Example of a non-task-add request:

User: "list all my tasks"
AI: "I'm sorry, I can only help you add tasks right now.".
               """
}


def run_agent_loop():
    conversation_history.append(context)
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
