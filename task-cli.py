import os
import sys
import json
from datetime import datetime
import cmd

FILE_NAME = "tasks.json"

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks)+1

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=2)

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return json.load(f)

class TaskCLI(cmd.Cmd):
    prompt = "task-cli > "

    def do_add(self,arg):
        """add <description>"""
        if not arg:
            print("Missing description")
            return

        tasks = load_tasks()
        task = {
            "id": get_next_id(tasks),
            "description": arg,
            "status": "todo",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        tasks.append(task)
        save_tasks(tasks)
        print(f"Added task (ID: {task['id']})")

    def do_update(self,arg):
        """update <id> <description>"""
        parts = arg.split()

        if len (parts) < 2:
            print("Usage: update <id> <description>")
            return

        task_id = int(parts[0])
        description = " ".join(parts[1:])

        tasks = load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["description"] = description
                task["updated_at"] = str(datetime.now())
                save_tasks(tasks)
                print("Updated task")
                return
        print("Task not found")

    def do_delete(self, arg):
        """delete <id>"""
        if not arg:
            print("Usage: delete <id>")
            return

        task_id = int(arg[0])
        tasks = load_tasks()
        new_tasks = [t for t in tasks if t["id"] != task_id]
        if len(tasks) == len(new_tasks):
            print("Task not found")
            return
        save_tasks(new_tasks)
        print("Deleted task")

    def do_mark(self, arg):
        """mark <id> <in-progress|done>"""
        parts = arg.split()

        if len(parts) < 2:
            print("Usage: mark <id> <in-progress|done>")
            return

        task_id = int(parts[0])
        status = parts[1]

        if status not in["in-progress", "done"]:
            print("Unknown status")
            return

        tasks = load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = str(datetime.now())
                save_tasks(tasks)
                print(f"Task marked as {status}")
                return
            print("Task not found")

    def do_list(self, arg):
        """list [status]"""
        tasks = load_tasks()
        if arg:
            tasks = [t for t in tasks if t["status"] == arg]

        if not tasks:
            print("No tasks")
            return

        for task in tasks:
            print(f"[{task['id']}] {task['description']} ({task['status']})")


    def do_exit(self,arg):
        """Exit CLI"""
        print("Goodbye")
        return True

    def do_quit(self, arg):
        return self.do_exit(arg)

    def do_EOF(self, arg):
        print()
        return True

if __name__ == "__main__":
    TaskCLI().cmdloop()