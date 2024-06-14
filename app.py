import tkinter as tk
from tkinter import messagebox
from managers.user_manager import UserManager


class App:
    def __init__(self, root, con):
        self.root = root
        self.root.title("Login")
        self.con = con

        self.user = None

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = UserManager.login(self.con, username, password)
        if user:
            self.user = user
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_main_screen(self):
        self.clear_screen()

        welcome_label = tk.Label(
            self.root, text=f"Welcome, {self.user.username} ({self.user.role})"
        )
        welcome_label.pack(pady=5)

        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=5)

        # Display role-based content
        if self.user.role == "super_admin":
            self.create_super_admin_screen()
        elif self.user.role == "system_admin":
            self.create_system_admin_screen()
        elif self.user.role == "consultant":
            self.create_consultant_screen()

    def create_super_admin_screen(self):
        label = tk.Label(self.root, text="Super Admin Panel")
        label.pack()

    def create_system_admin_screen(self):
        label = tk.Label(self.root, text="System Admin Panel")
        label.pack()

    def create_consultant_screen(self):
        label = tk.Label(self.root, text="Consultant Panel")
        label.pack()

    def logout(self):
        self.user = None
        self.create_login_screen()

    def run(self):
        self.root.mainloop()
