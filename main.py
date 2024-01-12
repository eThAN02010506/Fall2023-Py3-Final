import ttkbootstrap as tb
from K import *
from views import login, tasks, users


class TaskApp(tb.Window):

    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("854x640")

        # User variables
        self.authenticated = False
        self.email = tb.StringVar()
        self.token: dict = {}

        # Views variables
        self.current_view = None
        self.header_frame = None
        self.views = {
            "login": login.LoginView(self),
            "signup": users.UserView(self),
            "view_tasks": tasks.TasksView(self),
            "create_task": tasks.CreateTaskView(self),
            "view_task": tasks.TaskView(self)
        }

        # Init Welcome Screen
        self.create_header()
        self.show_login_view()

    def geturl(self, module):
        return "http://127.0.0.1:8000" + module

    def getauth(self):
        if self.token.get("token_type") != "bearer":
            return {}
        return {"Authorization": self.token.get("token_type") + " " + self.token.get("access_token")}

    def create_header(self):
        self.header_frame = tb.Frame(self, bootstyle=PRIMARY)

        logout_button = tb.Button(self.header_frame, text="Logout", command=self.logout, bootstyle=SECONDARY)
        logout_button.pack(side=RIGHT, padx=PS, pady=PXS)

    def show_header(self):
        self.header_frame.pack(fill=X)

    def hide_header(self):
        self.header_frame.pack_forget()

    def logout(self):
        self.authenticated = False
        self.show_login_view()

    def show_login_view(self):
        self.set_current_view("login")

    def show_signup_view(self):
        self.set_current_view("signup")

    def show_task_view(self, id):
        self.set_current_view("view_task")
        self.current_view.refresh(id)

    def show_tasks_view(self, refresh=False):
        if refresh:
            self.views["view_tasks"] = tasks.TasksView(self)
        self.set_current_view("view_tasks")

    def show_create_task_view(self):
        self.set_current_view("create_task")

    def set_current_view(self, key):
        self.destroy_current_view()
        self.current_view = self.views.get(key)
        if self.authenticated:
            self.show_header()
        else:
            self.hide_header()
        self.current_view.pack_view()

    def destroy_current_view(self):
        if self.current_view:
            self.current_view.unpack_view()


if __name__ == "__main__":
    app = TaskApp()
    app.place_window_center()
    app.mainloop()
