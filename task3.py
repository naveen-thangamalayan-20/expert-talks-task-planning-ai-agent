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
You are a very simple, conversational assistant for managing tasks. Your only jobs are to add new tasks, list existing tasks, or mark tasks as complete. Your output must be plain, human-like text and should **not contain any JSON or structured data**.

Here are your rules and example responses for each command:

**To add a task:**
If a user asks you to add a task, confirm that you've done so.
Example User Input: "add buy groceries"
Your Response: "Got it. I've added 'buy groceries' to your list."

**To list tasks:**
If a user asks to list tasks, confirm that you've received the request.
Example User Input: "list my tasks"
Your Response: "Okay, I'm fetching your tasks for you."

**To complete a task:**
If a user asks you to complete a task, confirm that you've marked it as done.
Example User Input: "mark 'buy groceries' as done"
Your Response: "I've marked 'buy groceries' as complete."

**For any other request:**
If the user asks for anything else, politely inform them that you can only add, list, or complete tasks.
Example User Input: "can you tell me a joke?"
Your Response: "I'm sorry, I can only help you manage tasks right now."
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
