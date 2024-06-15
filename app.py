import tkinter as tk
from tkinter import ttk
from config import Config
from tkinter import messagebox
from managers.address_manager import AddressManager
from managers.member_manager import MemberManager
from managers.profile_manager import ProfileManager
from managers.user_manager import UserManager
from forms.Form import *


class App:
    config: Config = None

    def __init__(self, root, config):
        self.root = root
        App.config = config

        self.user_manager = UserManager(config)
        self.address_manager = AddressManager(config)
        self.member_manager = MemberManager(config)
        self.profile_manager = ProfileManager(config)

        self.init_db()

        self.root.title("Login")
        self.user = None
        self.create_login_screen()

    def run(self):
        self.root.mainloop()

    def init_db(self):
        self.user_manager.initialize()
        self.user_manager.create_super_admin()
        self.address_manager.initialize()
        self.member_manager.initialize()
        self.profile_manager.initialize()

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

    def logout(self):
        self.user = None
        self.create_login_screen()

    def go_back(self):
        self.clear_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        username = "super_admin"
        password = "Admin_123?"

        user = self.user_manager.login(username, password)
        if user:
            self.user = user
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_main_screen(self):
        self.clear_screen()

        welcome_label = tk.Label(self.root, text=f"Welcome, {self.user.username}")
        welcome_label.pack(pady=5)

        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=5)

        # make dividers
        divider = tk.Label(self.root, text="---------------------------------")
        divider.pack(pady=5)

        # Display role-based content
        if self.user.role == "super_admin":
            self.create_super_admin_screen()
        elif self.user.role == "system_admin":
            self.create_system_admin_screen()
        elif self.user.role == "consultant":
            self.create_consultant_screen()

    #
    # Super admin screens
    #
    def create_super_admin_screen(self):
        self.clear_screen()

        def handle_option(option):
            if option == "Users":
                self.view_users()
            elif option == "Members":
                self.view_members()

        label = tk.Label(self.root, text="Super Admin Panel")
        label.pack()

        # print list of menu options
        menu_options = [
            "Users",
            "Members",
        ]

        for i, option in enumerate(menu_options):
            button = tk.Button(
                self.root,
                text=option,
                command=lambda option=option: handle_option(option),
            )
            button.pack(pady=5)

    #
    # System admin screens
    #
    def create_system_admin_screen(self):
        label = tk.Label(self.root, text="System Admin Panel")
        label.pack()

    #
    # Consultant screens
    #
    def create_consultant_screen(self):
        label = tk.Label(self.root, text="Consultant Panel")
        label.pack()

    def create_delete_screen(self):
        pass

    ###########################################################
    def view_users(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Users")
        label.pack()

        def handle_option(option):
            if option == "Create user":
                form = CreateUserForm(self.root, App.config, self.view_users)
                form.show_form()

            elif option == "Delete user":
                delete_form = DeleteUserForm(self.root, App.config, self.view_users)
                delete_form.show_form()

            elif option == "Update user":

                def on_username_click(event):
                    item = tree.selection()[0]
                    update_form = UpdateUserForm(self.root, App.config, self.view_users)
                    username = tree.item(item, "values")[0]
                    update_form.show_form(username)

                self.clear_screen()

                self.return_button = tk.Button(
                    self.root, text="Return", command=self.view_users
                )
                self.return_button.pack(pady=20)

                tree = ttk.Treeview(
                    self.root, columns=("Username", "Role"), show="headings"
                )
                tree.heading("Username", text="Username")
                tree.heading("Role", text="Role")
                tree.pack(padx=10, pady=10)

                users = self.user_manager.get_users()
                for user in users:
                    username = user.username
                    role = user.role
                    tree.insert("", "end", values=(username, role))

                tree.bind("<Double-1>", on_username_click)

        menu_options = [
            "Create user",
            "Delete user",
            "Update user",
        ]

        self.return_button = tk.Button(
            self.root, text="Return", command=self.get_correct_menu()
        )
        self.return_button.pack(pady=20)

        for i, option in enumerate(menu_options):
            button = tk.Button(
                self.root,
                text=option,
                command=lambda option=option: handle_option(option),
            )
            button.pack(pady=5)

    def view_members(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Members")
        label.pack()

        def handle_option(option):
            if option == "Create member":
                form = CreateMemberForm(self.root, App.config, self.view_members)
                form.show_form()
            elif option == "Delete member":
                delete_form = DeleteMemberForm(self.root, App.config, self.view_members)
                delete_form.show_form()
            elif option == "Update member":

                def on_member_id_click(event):
                    item = tree.selection()[0]
                    update_form = UpdateMemberForm(
                        self.root, App.config, self.view_members
                    )
                    member_id = tree.item(item, "values")[0]
                    update_form.show_form(int(member_id))

                self.clear_screen()

                self.return_button = tk.Button(
                    self.root, text="Return", command=self.view_members
                )
                self.return_button.pack(pady=20)

                tree = ttk.Treeview(
                    self.root,
                    columns=("Member ID", "First Name", "Last Name"),
                    show="headings",
                )
                tree.heading("Member ID", text="Member ID")
                tree.heading("First Name", text="First Name")
                tree.heading("Last Name", text="Last Name")
                tree.pack(padx=10, pady=10)

                members = self.member_manager.get_members()
                for member in members:
                    member_id = member.id
                    first_name = member.first_name
                    last_name = member.last_name
                    tree.insert("", "end", values=(member_id, first_name, last_name))

                tree.bind("<Double-1>", on_member_id_click)

        menu_options = [
            "Create member",
            "Delete member",
            "Update member",
        ]

        self.return_button = tk.Button(
            self.root, text="Return", command=self.get_correct_menu()
        )
        self.return_button.pack(pady=20)

        for i, option in enumerate(menu_options):
            button = tk.Button(
                self.root,
                text=option,
                command=lambda option=option: handle_option(option),
            )
            button.pack(pady=5)

    def get_correct_menu(self):
        if self.user.role == "super_admin":
            return self.create_super_admin_screen
        elif self.user.role == "system_admin":
            return self.create_system_admin_screen
        elif self.user.role == "consultant":
            return self.create_consultant_screen
