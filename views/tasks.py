import ttkbootstrap as tb
from views.helper import View
import requests as req
from tkinter import *
import tkinter as tk
from K import *

class TasksView(View):
    def __init__(self, app):
        super().__init__(app)
        self.background()    
        self.create_widgets()


    def background(self):
        # Load the background image
        background_image = tk.PhotoImage(file="Images/截屏2024-01-15 21.31.11.png")

        # Create a Label with the background image (couldn't figure out how to use ttkbootstrap to do this... so, used
        # tkinter.)
        background_label = tk.Label(self.frame, image=background_image)
        background_label.photo = background_image
        background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def create_widgets(self):
        container = tb.Frame(self.frame)
        container.place(relx=0.5,y=5,anchor=N)
        tb.Button(container, text="Create Task", command=self.app.show_create_task_view).grid(row = 0, column = 9,  pady = 2)
        tb.Label(container, text = "No tasks found").grid(row = 1, column = 4, columnspan=7,  pady = 2)

    def refresh(self):
        for child in self.frame.winfo_children():
            child.destroy()
        self.background()
        container = tb.Frame(self.frame)
        container.place(relx=0.5,y=5,anchor=N)
        
        tb.Button(container, text="Create Task", command=self.app.show_create_task_view).grid(row = 0, column = 9,  pady = 2)

        tasks = req.get(self.app.geturl("/tasks"), headers=self.app.getauth())
        if tasks.status_code != 200:
            tb.Label(container, text = "No tasks found").grid(row = 1, column = 4, columnspan=7,  pady = 2)
        else:
            tb.Label(container, text = "ID").grid(row = 1, column = 4,  pady = 2, ipadx=10)
            tb.Label(container, text = "Title").grid(row = 1, column = 5,  pady = 2, ipadx=30)
            tb.Label(container, text = "Priority").grid(row = 1, column = 6,  pady = 2, ipadx=10)
            tb.Label(container, text = "Complete").grid(row = 1, column = 7,  pady = 2, ipadx=10)
            tb.Label(container, text = "CreateTime").grid(row = 1, column = 8,  pady = 2, ipadx=50)
            tb.Label(container, text = "Operation").grid(row = 1, column = 9, columnspan=2,  pady = 2, ipadx=20)

            i = 2
            for task in tasks.json():
                oper = TaskOperation(self, self.app, task.get("id"))
                tb.Label(container, text = task.get("id")).grid(row = i, column = 4,  pady = 2, ipadx=10)
                tb.Label(container, text = task.get("title")).grid(row = i, column = 5,  pady = 2, ipadx=25)
                tb.Label(container, text = task.get("priority")).grid(row = i, column = 6,  pady = 2, ipadx=10)
                tb.Label(container, text = task.get("complete")).grid(row = i, column = 7,  pady = 2, ipadx=10)
                tb.Label(container, text = task.get("created_on")).grid(row = i, column = 8,  pady = 2, ipadx=50)
                tb.Button(container, text="Update", command=oper.show_task).grid(row = i, column = 9,  pady = 2, ipadx=10)
                tb.Button(container, text="Delete", command=oper.delete_task).grid(row = i, column = 50,  pady = 2, ipadx=10)
                i = i + 1


class TaskOperation:
    def __init__(self, owner, app, id):
        self.app = app
        self.owner = owner
        self.id = id

    def show_task(self):
        self.app.show_task_view(self.id)

    def delete_task(self):
        rsp = req.delete(self.app.geturl(f"/tasks/{self.id}"), headers=self.app.getauth())
        if rsp.status_code == 204:
            self.owner.create_toast("Task deleted", f"Task '{self.id}' deleted successfully")
            self.app.show_tasks_view(True)
        else:
            self.owner.create_toast("Task delete", f"Task '{self.id}' delete failed")


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
        tb.Button(container, text="Submit", command=self.update_task
            , bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W, side=LEFT)
        tb.Button(container, text="Cancel", command=self.app.show_tasks_view
            , bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W, side=LEFT)

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

        rsp = req.put(self.app.geturl(f"/tasks/{id}"),  json={ "id": id, "title": title, "description":desc, "priority":priority, "complete": complete }, headers=self.app.getauth())
        if rsp.status_code == 204:
            self.create_toast("Task Updated", f"Task '{title}' updated successfully")
            self.app.show_tasks_view(True)
        else:
            self.create_toast("Task Update", f"Task '{title}' update failed")
            self.app.show_tasks_view()


class CreateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.title = tb.StringVar()
        self.desc = tb.StringVar()
        self.priority = tb.IntVar(value=1)
        self.background()
        self.create_widgets()
    def background(self):                                                                                             
        # Load the background image
        background_image = tk.PhotoImage(file="Images/截屏2024-01-15 21.31.11.png")

        # Create a Label with the background image (couldn't figure out how to use ttkbootstrap to do this... so, used
        # tkinter.)
        background_label = tk.Label(self.frame, image=background_image)
        background_label.photo = background_image
        background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_widgets(self):
        container = tb.Frame(self.frame, bootstyle=INFO)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        tb.Label(container, text="Title:").pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.title).pack(padx=10, pady=10, anchor=W)
        tb.Label(container, text="Description:").pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.desc).pack(padx=10, pady=10, anchor=W)
        tb.Label(container, text="Priority:").pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.priority).pack(padx=10, pady=10, anchor=W)

        tb.Button(container, text="Create Task", command=self.create_task).pack(side=RIGHT, padx=5)
        tb.Button(container, text="Back", command=self.app.show_tasks_view).pack(side=RIGHT, padx=5)

    def create_task(self):
        title = self.title.get()
        desc = self.desc.get()
        priority = self.priority.get()

        rsp = req.post(self.app.geturl("/tasks"),  json={ "title": title, "description":desc, "priority":priority }, headers=self.app.getauth())
        if rsp.status_code == 201:
            self.create_toast("Task Created", f"Task '{title}' created successfully")
        else:
            self.create_toast("Task Create", f"Task '{title}' create failed")

        # After creating the task, show the task page
        self.app.show_tasks_view(True)
        