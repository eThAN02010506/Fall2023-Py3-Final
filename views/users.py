import json
import tkinter as tk
import ttkbootstrap as tb
from K import *
from views.helper import View
import requests as req

class UserView(View):
    def __init__(self, app):
        super().__init__(app)
        self.name = tb.StringVar()
        self.nickname = tb.StringVar()
        self.email = tb.StringVar()
        self.password = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Create a container frame to organize widgets
        container = tb.Frame(self.frame, bootstyle=SUPERHERO)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Email Label and Entry
        tb.Label(container, text="Name", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.name, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Password Label and Entry
        tb.Label(container, text="Nickname", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.nickname, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        tb.Label(container, text="Email", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.email, bootstyle=SUPERHERO).pack(padx=10, pady=10)

        tb.Label(container, text="Password", bootstyle=SUPERHERO).pack(padx=10, pady=10, anchor=W)
        tb.Entry(container, textvariable=self.password, show="*", bootstyle=SUPERHERO).pack(padx=10, pady=10)

        # Submit Button
        tb.Button(container, text="Submit", command=self.submit_user, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W
                                                                                              , side=LEFT)
        tb.Button(container, text="Cancel", command=self.cancel, bootstyle=SUCCESS).pack(padx=10, pady=10, anchor=W
                                                                                              , side=LEFT)

    def submit_user(self):
        name = self.email.get()
        nickname = self.password.get()
        email = self.email.get()
        password = self.password.get()

        # 调用API将用户信息插入数据库
        rsp = req.post(self.app.geturl("/users"), json = { "name": name, "alt_name":nickname, "email":email, "password":password, "role": "admin" })
        if rsp.status_code == 201:
            self.create_toast("User created", "User {name} created successfully")

            # 清空输入框
            self.email.set("")
            self.password.set("")

            # 返回到最开始的页面
            self.app.show_login_view()
        else:
            self.create_toast("User create", "User {name} create failed")

    def cancel(self):
         self.app.show_login_view()

