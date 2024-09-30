import tkinter as tk
from entities.user import User
from tkinter import messagebox
from managers.user_manager import UserManager
from managers.profile_manager import ProfileManager
from entities.user import User
from validations import (
    validate_username,
    validate_password,
    validate_name,
)
from forms.base_form import BaseForm


class CreateConsultantForm(BaseForm):
    def __init__(
        self,
        root,
        config,
        logger,
        sender,
        authorize,
        view_users_callback,
    ):
        authorized_roles = (User.Role.SYSTEM_ADMIN,)
        super().__init__(root, config, logger, sender, authorize, authorized_roles)
        self.user_manager = UserManager(config)
        self.profile_manager = ProfileManager(config)
        self.view_users_callback = view_users_callback

    def show_form(self):
        self.authorize(self.authorized_roles)
        self.clear_screen()

        # Create a title label
        title_label = tk.Label(
            self.root, text=f"Add new Consultant", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # username
        self.username_label = tk.Label(
            self.root, text="Please enter the new username", font=("Arial", 12)
        )
        self.username_label.pack(pady=5, padx=25)
        self.username_entry = tk.Entry(self.root, width=100)
        self.username_entry.pack(pady=5, padx=25)

        # password
        self.password_label = tk.Label(
            self.root, text="Please enter the new password", font=("Arial", 12)
        )
        self.password_label.pack(pady=5, padx=25)
        self.password_entry = tk.Entry(self.root, show="*", width=100)
        self.password_entry.pack(pady=5, padx=25)

        # first name
        self.first_name_label = tk.Label(
            self.root, text="Please enter the first name", font=("Arial", 12)
        )
        self.first_name_label.pack(pady=5, padx=25)
        self.first_name_entry = tk.Entry(self.root, width=100)
        self.first_name_entry.pack(pady=5, padx=25)

        # last name
        self.last_name_label = tk.Label(
            self.root, text="Please enter the last name", font=("Arial", 12)
        )
        self.last_name_label.pack(pady=5, padx=25)
        self.last_name_entry = tk.Entry(self.root, width=100)
        self.last_name_entry.pack(pady=5, padx=25)

        # submit button
        self.submit_button = tk.Button(self.root, text="Save", command=self.submit)
        self.submit_button.pack(pady=20)

        # back button
        self.back_button = tk.Button(
            self.root, text="Cancel", command=self.view_users_callback
        )
        self.back_button.pack(pady=20)

    def submit(self):
        self.authorize(self.authorized_roles)

        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        errors = []
        if not validate_username(username):
            errors.append("Username is not valid.")

        if not validate_password(password):
            errors.append("Password is not valid.")

        if not validate_name(first_name):
            errors.append("First name has to be between 2 and 20 characters.")

        if not validate_name(last_name):
            errors.append("Last name has to be between 2 and 20 characters.")

        if not self.user_manager.is_available_username(username):
            errors.append("Username is already taken.")

        if len(errors) == 0:
            user = self.user_manager.create_user(
                username, password, User.Role.CONSULTANT.value
            )
            self.logger.log_activity(
                self.sender,
                "created user",
                f"with username: {user.username}",
                False,
            )

            if user is not None:
                profile = self.profile_manager.create_profile(
                    first_name, last_name, user.id
                )
                if profile is not None:
                    messagebox.showinfo("Information", f"User has been created.")
                    self.view_users_callback()
        else:
            messages = "\n".join(errors)
            messagebox.showinfo("Information", messages)


class UpdateConsultantForm(BaseForm):
    def __init__(
        self,
        root,
        config,
        logger,
        sender,
        authorize,
        view_users_callback,
        view_password_reset,
    ):
        authorized_roles = (User.Role.SYSTEM_ADMIN,)
        super().__init__(root, config, logger, sender, authorize, authorized_roles)
        self.user_manager = UserManager(self.config)
        self.profile_manager = ProfileManager(self.config)
        self.view_users_callback = view_users_callback
        self.view_password_reset = view_password_reset

    def show_form(self, username):
        self.authorize(self.authorized_roles)

        # Get user and profile
        updated_user = self.user_manager.get_user(username)
        updated_profile = self.profile_manager.get_profile(updated_user.id)

        if updated_user.role != User.Role.CONSULTANT.value:
            messagebox.showerror(
                "Error",
                "Only consultants can be updated using this form, incident logged.",
            )
            self.logger.log_activity(
                self.sender,
                "attempted to update a non-consultant user using the consultant form",
                f"with username: {updated_user.username}",
                True,
            )
            return self.view_users_callback()

        self.clear_screen()

        # Create a title label
        title_label = tk.Label(
            self.root, text=f"Update Consultant", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # username
        self.current_username_label = tk.Label(
            self.root, text="Current Username", font=("Arial", 12)
        )
        self.current_username_label.pack(pady=5, padx=25)
        self.current_username_entry = tk.Entry(self.root, width=100)
        self.current_username_entry.insert(0, updated_user.username)
        self.current_username_entry.config(state="readonly")
        self.current_username_entry.pack(pady=5, padx=25)

        # first name
        self.first_name_label = tk.Label(
            self.root, text="Please enter the first name", font=("Arial", 12)
        )
        self.first_name_label.pack(pady=5, padx=25)
        self.first_name_entry = tk.Entry(self.root, width=100)
        self.first_name_entry.insert(0, updated_profile.first_name)
        self.first_name_entry.pack(pady=5, padx=25)

        # last name
        self.last_name_label = tk.Label(
            self.root, text="Please enter the last name", font=("Arial", 12)
        )
        self.last_name_label.pack(pady=5, padx=25)
        self.last_name_entry = tk.Entry(self.root, width=100)
        self.last_name_entry.insert(0, updated_profile.last_name)
        self.last_name_entry.pack(pady=5, padx=25)

        # reset password button
        self.reset_password_button = tk.Button(
            self.root,
            text="Reset Password",
            command=lambda: self.view_password_reset(updated_user.username),
        )
        self.reset_password_button.pack(pady=5)

        # submit button
        self.submit_button = tk.Button(self.root, text="Save", command=self.submit)
        self.submit_button.pack(pady=5)

        # delete button
        self.delete_button = tk.Button(
            self.root,
            text="Delete",
            command=self.delete,
            fg="red",
            font=("Arial", 12, "bold"),
        )
        self.delete_button.pack(pady=5)

        # back button
        self.back_button = tk.Button(
            self.root, text="Cancel", command=self.view_users_callback
        )
        self.back_button.pack(pady=5)

    def submit(self):
        self.authorize(self.authorized_roles)
        current_username = self.current_username_entry.get()
        new_first_name = self.first_name_entry.get()
        new_last_name = self.last_name_entry.get()

        try:
            user_to_update = self.user_manager.get_user(current_username)
            if user_to_update is not None:
                errors = []
                if not validate_name(new_first_name):
                    errors.append("First name has to be between 2 and 20 characters.")

                if not validate_name(new_last_name):
                    errors.append("Last name has to be between 2 and 20 characters.")

                if len(errors) == 0:
                    self.user_manager.update_user(
                        user_to_update, current_username, User.Role.CONSULTANT.value
                    )
                    updated_user = self.user_manager.get_user(current_username)
                    if updated_user is not None:
                        profile_to_update = self.profile_manager.get_profile(
                            user_to_update.id
                        )
                        updated_profile = self.profile_manager.update_profile(
                            profile_to_update, new_first_name, new_last_name
                        )
                        if updated_profile is not None:
                            messagebox.showinfo(
                                "Information", "User has been updated successfully."
                            )
                            self.logger.log_activity(
                                self.sender,
                                "updated user",
                                f"with username: {updated_user.username}",
                                False,
                            )
                            self.view_users_callback()
                    else:
                        messagebox.showerror(
                            "Error", "Failed to retrieve updated user."
                        )
                else:
                    messages = "\n".join(errors)
                    messagebox.showerror("Information", messages)
            else:
                messagebox.showerror("Error", "User not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")

    def delete(self):
        self.authorize(self.authorized_roles)
        current_username = self.current_username_entry.get()
        user = self.user_manager.get_user(current_username)
        self.user_manager.delete_user(user)
        messagebox.showinfo("Information", "User has been deleted.")

        self.logger.log_activity(
            self.sender, "deleted user", f"with username: {user.username}", False
        )
        self.view_users_callback()
