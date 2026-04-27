"""Laboratorio 8 - Módulo de persistencia para lista de tareas."""


def read_todo_file(file_path):
    """Reads tasks from a file. Returns a list of tasks."""
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"File {file_path} not found! Returning an empty to-do list.")
        return []


def write_todo_file(file_path, tasks):
    """Writes tasks to a file."""
    with open(file_path, 'w') as file:
        for task in tasks:
            file.write(task + "\n")

