import json

import requests

from tasks import create_task, completed_task, list_tasks

# --- Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:7b"  # Ensure you have 'qwen' model pulled in Ollama

def parse_json_string(llm_response):
    json_start = llm_response.find("{")
    json_end = llm_response.rfind("}")
    if json_start != -1 and json_end != -1 and json_start < json_end:
        json_string = llm_response[json_start: json_end + 1]
        return json.loads(json_string)
    else:
        raise Exception("Response not valid json")


def call_llm_message(prompt_messages):
    response = requests.post(OLLAMA_API_URL,
                             json={"model": OLLAMA_MODEL, "messages": prompt_messages, "stream": False,
                                   "format": "json"},
                             timeout=120)  # Increased timeout for local LLM
    response.raise_for_status()  # Raise an exception for HTTP errors
    llm_output = response.json()['message']['content']
    return parse_json_string(llm_output)


def perform_action(llm_message):
    if llm_message["intent"] == "add_task":
        return create_task(llm_message["task_description"])
    elif llm_message["intent"] == "complete_task":
        return completed_task(llm_message["task_description"])
    elif llm_message["intent"] == "list_tasks":
        result =  list_tasks()
        return result

conversation_history = []

context = {
    "role": "system",
    "content": """You are a conversational task manager Agent. Your primary goal is to help the user manager their task.
                  You understand commands to add tasks, list tasks, mark tasks as complete, query specific task or clear the task.
                  You must always respond in structure json format

                      Here's the expected JSON structure:
    {
        "intent": "add_task" | "list_tasks" | "complete_task",
        "task_description": "string or null for list/clear/unknown intents",
        "response_message": "string (a helpful, concise message to the user)"
    }

     - If the user asks to add a task, set 'intent' to 'add_task' and extract 'task_description'.
     - If the user asks to list tasks, set 'intent' to 'list_tasks'.
     - If the user asks to complete a task, set 'intent' to 'complete_task' and extract 'task_description'.
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

        # Add user's message to the conversation history
        conversation_history.append(({"role": "user", "content": user_input}))
        # Call the LLM with the updated history
        result = call_llm_message(conversation_history)
        # Perform the action based on the parsed LLM's response
        action_result = perform_action(result)
        # Add the agent's response to the conversation history for contextZ
        conversation_history.append({"role": "assistant", "content": action_result})
        # Display the result to the user
        print(f"Agent: {action_result}")


run_agent_loop()
