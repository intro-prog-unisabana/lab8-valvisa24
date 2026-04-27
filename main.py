import sys
from todo_manager import read_todo_file, write_todo_file


def main():
    try:
        if len(sys.argv) < 2:
            raise IndexError("Insufficient arguments provided!")

        if sys.argv[1] == "--help":
            print("""Usage: python main.py <file_path> <command> [arguments]...

Commands:
  add "task"    - Add a task to the list.
  remove "task" - Remove a task from the list.
  view          - Display all tasks.

Examples:
  python main.py tasks.txt add "Buy groceries"
  python main.py tasks.txt remove "Do laundry"
  python main.py tasks.txt view
  python main.py tasks.txt add "Call mom" remove "Take out trash" view""")
            return

        file_path = sys.argv[1]
        tasks = read_todo_file(file_path)

        i = 2 

        while i < len(sys.argv):
            command = sys.argv[i]

            if command == "view":
                print("Tasks:")
                for t in tasks:
                    print(t)
                i += 1

            elif command == "add":
                if i + 1 >= len(sys.argv):
                    raise IndexError('Task description required for "add".')

                task = sys.argv[i + 1]
                tasks.append(task)
                print(f'Task "{task}" added.')
                i += 2

            elif command == "remove":
                if i + 1 >= len(sys.argv):
                    raise IndexError('Task description required for "remove".')

                task = sys.argv[i + 1]

                if task in tasks:
                    tasks.remove(task)
                    print(f'Task "{task}" removed.')
                else:
                    print(f'Task "{task}" not found.')

                i += 2

            else:
                raise ValueError("Command not found!")

        write_todo_file(file_path, tasks)

    except IndexError as e:
        print(e)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()