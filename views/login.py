import json
import tkinter as tk
import ttkbootstrap as tb
from K import *
from views.helper import View
import requests as req

class LoginView(View):

    def __init__(self, app):
        super().__init__(app)
        self.email = tb.StringVar()
        self.password = tb.StringVar()

        self.background()
        self.create_widgets()

    def background(self):
        # Load the background image
        background_image = tk.PhotoImage(file="Images/截屏2024-01-15 21.30.55.png")

        # Create a Label with the background image (couldn't figure out how to use ttkbootstrap to do this... so, used
        # tkinter. )
        background_label = tk.Label(self.frame, image=background_image)
        background_label.photo = background_image
        background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    def create_widgets(self):
        # Create a container frame to organize widgets

        container = tb.Frame(self.frame, bootstyle=SUPERHERO)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Email Label and Entry
        tb.Label(container, text="Email address：", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.email, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Password Label and Entry
        tb.Label(container, text="Password：", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.password, show="*", bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Login Button
        tb.Button(container, text="Login", command=self.login, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W,side=RIGHT)
        tb.Button(container, text="Sign up", command=self.signup, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W, side=LEFT)
          # 使按钮出现在container的正下方

    def signup(self):
        self.app.show_signup_view()

    def login(self):
        # Authentication methods
        email = self.email.get()
        password = self.password.get()

        rsp = req.post(self.app.geturl("/token"), data = { "username":email, "password":password })
        token = rsp.json()
        if token.get("token_type") == "bearer":
            self.app.authenticated = TRUE
            self.app.token = token
            self.app.email = email
            self.password.set("")
            self.app.show_tasks_view(True)
        else:
            self.create_toast("401 error", "authentication failed")
