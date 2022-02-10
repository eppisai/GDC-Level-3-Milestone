from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def __increment_priority(self, priority):
        if priority in self.current_items:
            self.__increment_priority(priority+1)
        self.current_items[priority] = self.current_items[priority - 1]

    def add(self, args):
        priority = int(args[0])
        if priority in self.current_items:
            self.__increment_priority(priority + 1)
        task = " ".join(args[1:])
        self.current_items[priority] = task
        self.write_current()
        print(f'Added task: "{task}" with priority {priority}')

    def done(self, args):
        priority = int(args[0])
        if priority in self.current_items:
            self.completed_items.append(self.current_items[priority])
            del self.current_items[priority]
            print('Marked item as done.')
        else:
            print(
                f"Error: no incomplete item with priority {priority} exists.")

        self.write_completed()
        self.write_current()

    def delete(self, args):
        priority = int(args[0])
        if self.current_items.pop(priority, None):
            self.write_current()
            print(f"Deleted item with priority {priority}")
        else:
            print(
                f"Error: item with priority {priority} does not exist. Nothing deleted."
            )

    def ls(self):
        i = 1
        for key, value in self.current_items.items():
            print(f"{i}. {value} [{key}]")
            i = i + 1

    def report(self):
        print(f"Pending : {len(self.current_items)}")
        i = 1
        for key, value in self.current_items.items():
            print(f"{i}. {value} [{key}]")
            i = i + 1
        i = 1
        print(f"\nCompleted : {len(self.completed_items)}")
        for item in self.completed_items:
            print(f"{i}. {item}")
            i = i + 1

    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        self.read_current()
        if len(self.current_items) == 0:
            return "<h1> There are no pending tasks! </h1>"

        text = "<h1> Incomplete Tasks : </h1> <h4> <ol>"
        current_items_list = sorted(self.current_items.items(), key=lambda x:x[0])
        for i in range(len(current_items_list)):
            text += f"<li> {str(current_items_list[i][1])} [ {str(current_items_list[i][0])} ] </li> <br>"
        
        text += "</ol> </h4>"
        return text

    def render_completed_tasks(self):
        # Complete this method to return all completed tasks as HTML
        self.read_completed()
        if len(self.completed_items) == 0:
            return "<h1> There are no completed tasks! </h1>"
            
        text = "<h1> Completed Tasks : </h1> <h4> <ol>"
        for completed_item in self.completed_items:
            text += f"<li> {completed_item} </li> <br>"

        text += "</ol> </h4>"
        return text


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
