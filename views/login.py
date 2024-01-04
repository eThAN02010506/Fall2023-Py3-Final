import ttkbootstrap as tb
from K import *
from views.helper import View


class LoginView(View):
    def __init__(self, app):
        super().__init__(app)
        self.email_var = tb.StringVar()
        self.password_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Email:").pack()
        tb.Entry(self.frame, textvariable=self.email_var).pack()
        tb.Label(self.frame, text="Password:").pack()
        tb.Entry(self.frame, textvariable=self.password_var, show="*").pack()
        tb.Button(self.frame, text="Login", command=self.login, bootstyle=SUCCESS).pack()

    def login(self):
        # Your authentication would need to be implemented here
        email = self.email_var.get()
        password = self.password_var.get()

        if email == "admin" and password == "password":
            self.app.authenticated = TRUE
            self.app.token = {"access_token": "string", "token_type": "bearer"}
            self.app.email = email
            self.password_var.set("")
            self.app.show_tasks_view()
        else:
            self.create_toast("401 Error", "Bad Credentials")
