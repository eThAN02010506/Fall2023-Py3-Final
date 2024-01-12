import json
import tkinter as tk
import ttkbootstrap as tb
from K import *
from views.helper import View
import requests as req

class LoginView(View):

    def __init__(self, app):
        super().__init__(app)
        self.email_var = tb.StringVar()
        self.password_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Create a container frame to organize widgets
        container_frame = tb.Frame(self.frame, bootstyle=SUPERHERO)
        container_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Email Label and Entry
        tb.Label(container_frame, text="Email address：", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container_frame, textvariable=self.email_var, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Password Label and Entry
        tb.Label(container_frame, text="Password：", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container_frame, textvariable=self.password_var, show="*", bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Login Button
        tb.Button(container_frame, text="Login", command=self.login, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W,side=RIGHT)
        tb.Button(container_frame, text="Sign up", command=self.signup, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W, side=LEFT)
          # 使按钮出现在container_frame的正下方

    def signup(self):
        self.app.show_signup_view()

    def login(self):
        # Authentication methods
        email = self.email_var.get()
        password = self.password_var.get()

        rsp = req.post(self.app.geturl("/token"), data = { "username":email, "password":password })
        token = rsp.json()
        if token.get("token_type") == "bearer":
            self.app.authenticated = TRUE
            self.app.token = token
            self.app.email = email
            self.password_var.set("")
            self.app.show_tasks_view(True)
        else:
            self.create_toast("401 error", "authentication failed")
