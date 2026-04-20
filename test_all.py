import subprocess
import sys
from pathlib import Path

import pytest

from todo_manager import read_todo_file, write_todo_file


ROOT = Path(__file__).resolve().parent


def run_script(script_name, *args):
    process = subprocess.run(
        [sys.executable, str(ROOT / script_name), *args],
        capture_output=True,
        text=True,
    )
    return process.returncode, process.stdout, process.stderr


class TestQuestion1:
    def test_valid_input(self):
        code, stdout, stderr = run_script("question1.py", "1000", "4")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == "Load per support point: 250.00 N"

    def test_zero_division(self):
        code, stdout, stderr = run_script("question1.py", "500", "0")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == (
            "Error: Cannot divide by zero! Supports must be greater than zero."
        )

    def test_non_numeric_input(self):
        code, stdout, stderr = run_script("question1.py", "1000", "five")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == "Error: Invalid input! Enter numeric values only."

    def test_missing_arguments(self):
        code, stdout, stderr = run_script("question1.py", "1000")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == "Error: Invalid input! Enter numeric values only."


class TestTodoManager:
    def test_read_todo_file_existing_file(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\nDo laundry\n", encoding="utf-8")

        tasks = read_todo_file(str(tasks_file))

        assert tasks == ["Buy groceries", "Do laundry"]

    def test_read_todo_file_missing_file(self, tmp_path, capsys):
        missing = tmp_path / "missing.txt"

        tasks = read_todo_file(str(missing))
        captured = capsys.readouterr()

        assert tasks == []
        assert captured.out.strip() == (
            f"File {missing} not found! Returning an empty to-do list."
        )

    def test_write_todo_file(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"

        write_todo_file(str(tasks_file), ["Task A", "Task B"])

        assert tasks_file.read_text(encoding="utf-8") == "Task A\nTask B\n"


class TestMainProgram:
    def test_insufficient_arguments(self):
        code, stdout, stderr = run_script("main.py")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == "Insufficient arguments provided!"

    def test_help(self):
        code, stdout, stderr = run_script("main.py", "--help")

        assert code == 0
        assert stderr == ""
        assert "Usage: python main.py <file_path> <command> [arguments]..." in stdout
        assert 'add "task"' in stdout
        assert 'remove "task"' in stdout
        assert "view" in stdout

    def test_no_command_exits_silently(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\n", encoding="utf-8")

        code, stdout, stderr = run_script("main.py", str(tasks_file))

        assert code == 0
        assert stderr == ""
        assert stdout == ""

    def test_view_with_missing_file(self, tmp_path):
        missing = tmp_path / "missing.txt"

        code, stdout, stderr = run_script("main.py", str(missing), "view")

        assert code == 0
        assert stderr == ""
        assert (
            stdout
            == f"File {missing} not found! Returning an empty to-do list.\nTasks:\n"
        )
        assert missing.read_text(encoding="utf-8") == ""

    def test_invalid_command(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\n", encoding="utf-8")

        code, stdout, stderr = run_script("main.py", str(tasks_file), "delete")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == "Command not found!"

    def test_view(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\nDo laundry\n", encoding="utf-8")

        code, stdout, stderr = run_script("main.py", str(tasks_file), "view")

        assert code == 0
        assert stderr == ""
        assert stdout == "Tasks:\nBuy groceries\nDo laundry\n"

    def test_add_without_task(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Task 1\n", encoding="utf-8")

        code, stdout, stderr = run_script("main.py", str(tasks_file), "add")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == 'Task description required for "add".'

    def test_remove_without_task(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Task 1\n", encoding="utf-8")

        code, stdout, stderr = run_script("main.py", str(tasks_file), "remove")

        assert code == 0
        assert stderr == ""
        assert stdout.strip() == 'Task description required for "remove".'

    def test_add_and_persist(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\n", encoding="utf-8")

        code, stdout, stderr = run_script(
            "main.py",
            str(tasks_file),
            "add",
            "Finish project",
            "view",
        )

        assert code == 0
        assert stderr == ""
        assert stdout == 'Task "Finish project" added.\nTasks:\nBuy groceries\nFinish project\n'
        assert tasks_file.read_text(encoding="utf-8") == "Buy groceries\nFinish project\n"

    def test_remove_existing(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\nDo laundry\n", encoding="utf-8")

        code, stdout, stderr = run_script(
            "main.py",
            str(tasks_file),
            "remove",
            "Do laundry",
            "view",
        )

        assert code == 0
        assert stderr == ""
        assert stdout == 'Task "Do laundry" removed.\nTasks:\nBuy groceries\n'
        assert tasks_file.read_text(encoding="utf-8") == "Buy groceries\n"

    def test_remove_non_existing(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\n", encoding="utf-8")

        code, stdout, stderr = run_script(
            "main.py",
            str(tasks_file),
            "remove",
            "Exercise",
            "view",
        )

        assert code == 0
        assert stderr == ""
        assert stdout == 'Task "Exercise" not found.\nTasks:\nBuy groceries\n'
        assert tasks_file.read_text(encoding="utf-8") == "Buy groceries\n"

    def test_multiple_commands_in_one_run(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\nFinish project\n", encoding="utf-8")

        code, stdout, stderr = run_script(
            "main.py",
            str(tasks_file),
            "add",
            "Call mom",
            "remove",
            "Buy groceries",
            "view",
        )

        assert code == 0
        assert stderr == ""
        assert stdout == 'Task "Call mom" added.\nTask "Buy groceries" removed.\nTasks:\nFinish project\nCall mom\n'
        assert tasks_file.read_text(encoding="utf-8") == "Finish project\nCall mom\n"

    def test_invalid_command_does_not_persist_partial_changes(self, tmp_path):
        tasks_file = tmp_path / "tasks.txt"
        tasks_file.write_text("Buy groceries\n", encoding="utf-8")

        code, stdout, stderr = run_script(
            "main.py",
            str(tasks_file),
            "add",
            "Call mom",
            "unknown_command",
        )

        assert code == 0
        assert stderr == ""
        assert stdout == 'Task "Call mom" added.\nCommand not found!\n'
        assert tasks_file.read_text(encoding="utf-8") == "Buy groceries\n"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
