import ttkbootstrap as tb
from views.helper import View
import requests
import requests as req

from tkinter import *
from tkinter.ttk import *
from K import *


class TasksView(View):
    def __init__(self, app):
        super().__init__(app)
        self.create_widgets()

    def create_widgets(self):
        tb.Button(self.frame, text="Create Task", command=self.app.show_create_task_view).grid(row=0, column=5,
                                                                                               sticky=W, pady=2)
        tasks = requests.get(self.app.geturl("/tasks"), headers=self.app.getauth())
        if tasks.status_code != 200:
            tb.Label(self.frame, text="No tasks found").grid(row=1, column=0, columnspan=7, sticky=W, pady=2)
        else:
            tb.Label(self.frame, text="ID").grid(row=1, column=0, sticky=W, pady=2)
            tb.Label(self.frame, text="Title").grid(row=1, column=1, sticky=W, pady=2)
            tb.Label(self.frame, text="Priority").grid(row=1, column=2, sticky=W, pady=2)
            tb.Label(self.frame, text="Complete").grid(row=1, column=3, sticky=W, pady=2)
            tb.Label(self.frame, text="CreateTime").grid(row=1, column=4, sticky=W, pady=2)
            tb.Label(self.frame, text="Operation").grid(row=1, column=5, columnspan=2, sticky=W, pady=2)

            i = 2
            for task in tasks.json():
                oper = TaskOperation(self, self.app, task.get("id"))
                tb.Label(self.frame, text=task.get("id")).grid(row=i, column=0, sticky=W, pady=2)
                tb.Label(self.frame, text=task.get("title")).grid(row=i, column=1, sticky=W, pady=2)
                tb.Label(self.frame, text=task.get("priority")).grid(row=i, column=2, sticky=W, pady=2)
                tb.Label(self.frame, text=task.get("complete")).grid(row=i, column=3, sticky=W, pady=2)
                tb.Label(self.frame, text=task.get("created_on")).grid(row=i, column=4, sticky=W, pady=2)
                tb.Button(self.frame, text="Update", command=oper.show_task).grid(row=i, column=5, sticky=W, pady=2)
                tb.Button(self.frame, text="Delete", command=oper.delete_task).grid(row=i, column=6, sticky=W, pady=2)
                i = i + 1


class TaskOperation:
    def __init__(self, owner, app, id):
        self.app = app
        self.owner = owner
        self.id = id

    def delete_task(self):
        rsp = req.delete(self.app.geturl(f"/tasks/{self.id}"), headers=self.app.getauth())
        if rsp.status_code == 204:
            self.owner.create_toast("Task deleted", f"Task '{self.id}' deleted successfully")
            self.app.show_tasks_view(True)
        else:
            self.owner.create_toast("Task delete", f"Task '{self.id}' delete failed")

    def show_task(self):
        self.app.show_task_view(self.id)


class TaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.id = tb.IntVar(value=0)
        self.title = tb.StringVar()
        self.desc = tb.StringVar()
        self.priority = tb.IntVar(value=1)
        self.complete = tb.BooleanVar(value=False)
        self.create_widgets()

    def create_widgets(self):
        # Create a container frame to organize widgets
        container = tb.Frame(self.frame, bootstyle=SUPERHERO)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Email Label and Entry
        tb.Label(container, text="Title", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.title, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Password Label and Entry
        tb.Label(container, text="Description", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.desc, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        tb.Label(container, text="Priority", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.priority, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        tb.Label(container, text="Complete", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.complete, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Submit Button
        tb.Button(container, text="Submit", command=self.update_task, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W
                                                                                              , side=LEFT)
        tb.Button(container, text="Cancel", command=self.cancel, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W
                                                                                         , side=LEFT)

    def refresh(self, id):
        rsp = req.get(self.app.geturl(f"/tasks/{id}"), headers=self.app.getauth())
        if rsp.status_code == 200:
            task = rsp.json()
            self.id.set(task.get("id"))
            self.title.set(task.get("title"))
            self.desc.set(task.get("description"))
            self.priority.set(task.get("priority"))
            self.complete.set(task.get("complete"))

    def update_task(self):
        id = self.id.get()
        title = self.title.get()
        desc = self.desc.get()
        priority = self.priority.get()
        complete = self.complete.get()

        rsp = req.put(self.app.geturl(f"/tasks/{id}"),
                      json={"id": id, "title": title, "description": desc, "priority": priority, "complete": complete},
                      headers=self.app.getauth())
        if rsp.status_code == 204:
            self.create_toast("Task Updated", f"Task '{title}' updated successfully")
            self.app.show_tasks_view(True)
        else:
            self.create_toast("Task Update", f"Task '{title}' update failed")
            self.app.show_tasks_view()

    def cancel(self):
        self.app.show_tasks_view()


class CreateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.title = tb.StringVar()
        self.desc = tb.StringVar()
        self.priority = tb.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Title:").pack()
        tb.Entry(self.frame, textvariable=self.title).pack()
        tb.Label(self.frame, text="Description:").pack()
        tb.Entry(self.frame, textvariable=self.desc).pack()
        tb.Label(self.frame, text="Priority:").pack()
        tb.Entry(self.frame, textvariable=self.priority).pack()

        tb.Button(self.frame, text="Create Task", command=self.create_task).pack(side=RIGHT, padx=5)
        tb.Button(self.frame, text="Back", command=self.app.show_tasks_view).pack(side=RIGHT, padx=5)

    def create_task(self):
        title = self.title.get()
        desc = self.desc.get()
        priority = self.priority.get()

        rsp = req.post(self.app.geturl("/tasks"), json={"title": title, "description": desc, "priority": priority},
                       headers=self.app.getauth())
        if rsp.status_code == 201:
            self.create_toast("Task Created", f"Task '{title}' created successfully")
        else:
            self.create_toast("Task Create", f"Task '{title}' create failed")

        # After creating the task, show the task page
        self.app.show_tasks_view(True)
