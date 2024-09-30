from tkinter import messagebox
from entities.user import User
from forms.base_form import BaseForm
from managers.user_manager import UserManager
import tkinter as tk
from utils import validate_password
from exceptions import LogoutException


class UserResetForm(BaseForm):
    def __init__(self, root, config, logger, sender, authorize, reset_callback):
        authorized_roles = (
            User.Role.SUPER_ADMIN,
            User.Role.SYSTEM_ADMIN,
            User.Role.CONSULTANT,
        )
        super().__init__(root, config, logger, sender, authorize, authorized_roles)
        self.user_manager = UserManager(config)
        self.reset_callback = reset_callback

    def show_form(self, reseted_username: str):
        try:
            self.authorize(self.authorized_roles)
            self.clear_screen()

            title_label = tk.Label(
                self.root, text="Reset Password", font=("Arial", 16, "bold")
            )
            title_label.pack(pady=10)

            self.current_username_label = tk.Label(
                self.root, text="Current Username", font=("Arial", 12)
            )
            self.current_username_label.pack(pady=5, padx=25)
            self.current_username_entry = tk.Entry(self.root, width=100)
            self.current_username_entry.insert(0, reseted_username)
            self.current_username_entry.config(state="readonly")
            self.current_username_entry.pack(pady=5, padx=25)

            self.password_label = tk.Label(
                self.root, text="Enter new password", font=("Arial", 12)
            )
            self.password_label.pack(pady=5, padx=25)

            self.password_entry = tk.Entry(self.root, show="*", width=100)
            self.password_entry.pack(pady=5, padx=25)

            self.submit_button = tk.Button(
                self.root, text="Reset Password", command=self.submit
            )
            self.submit_button.pack(pady=20)
        except LogoutException:
            # This will stop further execution after logout
            return

    def submit(self):
        self.authorize(self.authorized_roles)
        reseted_user = self.user_manager.get_user(self.current_username_entry.get())
        password = self.password_entry.get()

        if validate_password(password):
            self.user_manager.reset_password(reseted_user, password)
            messagebox.showinfo("Information", "User password has been set.")
            self.user_manager.reset_password_status(reseted_user)
            self.logger.log_activity(
                self.sender,
                "reset their own password",
                f"with role: {reseted_user.role}",
                False,
            )
            self.reset_callback()
        else:
            messagebox.showinfo("Information", "Please try Again")


class OtherResetForm(BaseForm):
    def __init__(self, root, config, logger, sender, authorize, reset_callback):
        authorized_roles = (User.Role.SUPER_ADMIN, User.Role.SYSTEM_ADMIN)
        super().__init__(root, config, logger, sender, authorize, authorized_roles)
        self.user_manager = UserManager(config)
        self.reset_callback = reset_callback

    def show_form(self, reseted_username: str):
        self.authorize(self.authorized_roles)
        self.clear_screen()

        title_label = tk.Label(
            self.root, text="Reset Password", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        self.current_username_label = tk.Label(
            self.root, text="Current Username", font=("Arial", 12)
        )
        self.current_username_label.pack(pady=5, padx=25)
        self.current_username_entry = tk.Entry(self.root, width=100)
        self.current_username_entry.insert(0, reseted_username)
        self.current_username_entry.config(state="readonly")
        self.current_username_entry.pack(pady=5, padx=25)

        self.password_label = tk.Label(
            self.root, text="Enter new password", font=("Arial", 12)
        )
        self.password_label.pack(pady=5, padx=25)

        self.password_entry = tk.Entry(self.root, show="*", width=100)
        self.password_entry.pack(pady=5, padx=25)

        self.submit_button = tk.Button(
            self.root, text="Reset Password", command=self.submit
        )
        self.submit_button.pack(pady=20)

    def submit(self):
        self.authorize(self.authorized_roles)
        reseted_user = self.user_manager.get_user(self.current_username_entry.get())
        password = self.password_entry.get()

        if validate_password(password):
            self.user_manager.reset_password(reseted_user, password)
            messagebox.showinfo("Information", "User temporary password has been set.")
            self.user_manager.reset_password_status(reseted_user, True)
            self.logger.log_activity(
                self.sender,
                "reset password of user",
                f"with username: {reseted_user.username}",
                False,
            )
            self.reset_callback()
        else:
            messagebox.showinfo("Information", "Please try Again")
