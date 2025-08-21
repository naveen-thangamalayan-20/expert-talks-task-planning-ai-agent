import json
import os

TASKS_FILE = "tasks.json"


def _load_tasks():
    """Loads tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def _save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def create_task(task_description):
    """
    Adds a new task to the list and saves it to the JSON file.
    """
    tasks = _load_tasks()
    tasks.append({
        "task_description": task_description,
        "status": "New"
    })
    _save_tasks(tasks)
    return f"Task '{task_description}' created successfully."


def completed_task(task_description):
    """
    Marks a task as completed and saves the changes.
    """
    tasks = _load_tasks()
    task_found = False
    for task in tasks:
        if task["task_description"].lower() == task_description.lower():
            task["status"] = "Completed"
            task_found = True
            break

    if task_found:
        _save_tasks(tasks)
        return f"Task '{task_description}' marked as completed."
    else:
        return f"Task '{task_description}' not found."


def list_tasks():
    """
    Lists all tasks and their status from the JSON file.
    """
    tasks = _load_tasks()
    if not tasks:
        return "No tasks found."

    output = "Current Tasks:\n"
    for i, task in enumerate(tasks, 1):
        output += f"{i}. {task['task_description']} [{task['status']}]\n"

    return output