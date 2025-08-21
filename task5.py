import json
import requests

# Assuming 'tasks.py' contains these functions
from tasks import create_task, completed_task, list_tasks

# --- Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:7b"

# --- Tool Definitions ---
# These describe the functions the LLM can call.
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Creates a new task with a description. Use this when the user wants to add a new item to their to-do list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "The description of the new task to be added."
                    }
                },
                "required": ["task_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "completed_task",
            "description": "Marks a task as completed. Use this when the user specifies a task they have finished.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "The description of the task to be marked as completed."
                    }
                },
                "required": ["task_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Lists all current tasks. Use this when the user asks to see their to-do list.",
            "parameters": {
                "type": "object",
                "properties": {}  # No parameters needed for this function.
            }
        }
    }
]


# --- LLM API Call Function ---
def call_llm_message(prompt_messages):
    """
    Calls the Ollama API with tool definitions.
    """
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": prompt_messages,
            "stream": False,
            "tools": tools,  # Pass the tools to the LLM
            "tool_choice": "auto"  # Let the LLM decide which tool to call
        },
        timeout=120
    )
    response.raise_for_status()
    # The response will now contain a tool_calls array if a tool was invoked
    return response.json()['message']


# --- Action and Agent Loop ---
def perform_action(llm_response_message):
    """
    Executes the tool call specified by the LLM's response.
    """
    tool_calls = llm_response_message.get('tool_calls')
    if not tool_calls:
        print("LLM did not identify a tool to call.")
        return llm_response_message.get('content', 'I am not sure how to respond.')

    # Iterate through all tool calls the LLM suggests
    for tool_call in tool_calls:
        function_name = tool_call['function']['name']
        function_args = tool_call['function']['arguments']

        print(f"Calling tool: {function_name} with arguments: {function_args}")

        # Use a dictionary to map function names to actual functions
        function_map = {
            "create_task": create_task,
            "completed_task": completed_task,
            "list_tasks": list_tasks
        }

        if function_name in function_map:
            # Call the function with the extracted arguments
            result = function_map[function_name](**function_args)
            return result
        else:
            return f"Error: Unknown tool '{function_name}'"


def run_agent_loop():
    """
    Main loop to interact with the user and the LLM.
    """
    conversation_history = [
        {
            "role": "system",
            "content": "You are a conversational task manager AI. You can add, complete, and list tasks. Use the provided tools to manage tasks."
        }
    ]

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        elif not user_input:
            continue

        # Add user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Call the LLM with the updated history
        llm_response = call_llm_message(conversation_history)

        # Perform the action based on the LLM's response
        action_result = perform_action(llm_response)

        # Display the result to the user
        print(f"Agent: {action_result}")

        # Add the agent's response to the conversation history for context
        # Note: In a full implementation, you'd add both the tool call and the tool output
        # to the history for a complete context chain.
        conversation_history.append({"role": "assistant", "content": action_result})


# Start the agent
if __name__ == "__main__":
    run_agent_loop()