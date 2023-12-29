import ttkbootstrap as tb
from views.helper import View


class TasksView(View):
    def __init__(self, app):
        super().__init__(app)
        self.create_widgets()

    def create_widgets(self):
        # Add code to display a list of tasks here

        tb.Button(self.frame, text="To task detail", command=self.app.show_task_view).pack()
        tb.Button(self.frame, text="Create Task", command=self.app.show_create_task_view).pack()


class TaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Task Manager").pack()
        tb.Button(self.frame, text="Back to View Tasks", command=self.app.show_tasks_view).pack()


class CreateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.task_name_var = tb.StringVar()
        self.task_description_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Task Name:").pack()
        tb.Entry(self.frame, textvariable=self.task_name_var).pack()
        tb.Label(self.frame, text="Description:").pack()
        tb.Entry(self.frame, textvariable=self.task_description_var).pack()

        tb.Button(self.frame, text="Create Task", command=self.create_task).pack()
        tb.Button(self.frame, text="Back", command=self.app.show_task_view).pack()

    def create_task(self):
        # Add your code to create a task here
        task_name = self.task_name_var.get()
        task_description = self.task_description_var.get()

        self.create_toast("Task Created", f"Task '{task_name}' created successfully")

        # After creating the task, show the task page
        self.app.show_task_view()
