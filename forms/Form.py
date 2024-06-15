import tkinter as tk
from tkinter import ttk
from entities.user import User
from tkinter import messagebox
from managers.profile_manager import ProfileManager
from managers.user_manager import UserManager
from managers.member_manager import MemberManager
from managers.address_manager import AddressManager
from config import Config
from entities.member import Member
from entities.address import Address
from validations import *


class BaseForm:
    def __init__(self, root):
        self.root = root

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Users
class CreateUserForm(BaseForm):
    config: Config = None

    def __init__(self, root, config, view_users_callback):
        super().__init__(root)
        CreateUserForm.config = config
        self.user_manager = UserManager(config)
        self.profile_manager = ProfileManager(config)

        self.view_users_callback = view_users_callback

    def show_form(self):
        self.clear_screen()
        # Create a title label
        title_label = tk.Label(
            self.root, text="Create new user", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # return button
        self.return_button = tk.Button(
            self.root, text="Return", command=self.view_users_callback
        )
        self.return_button.pack(pady=20)

        # username
        self.username_label = tk.Label(
            self.root, text="Please enter the new username", font=("Arial", 12)
        )
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=100)
        self.username_entry.pack(pady=5)

        # password
        self.password_label = tk.Label(
            self.root, text="Please enter the new password", font=("Arial", 12)
        )
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=100)
        self.password_entry.pack(pady=5)

        # role
        self.role_label = tk.Label(
            self.root, text="Select an role:", width=100, font=("Arial", 12)
        )
        self.role_label.pack(pady=10)
        options = [User.Role.CONSULTANT.value, User.Role.SYSTEM_ADMIN.value]
        self.roles_option = ttk.Combobox(self.root, values=options)
        self.roles_option.pack()

        # first name
        self.first_name_label = tk.Label(
            self.root, text="Please enter the first name", font=("Arial", 12)
        )
        self.first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, width=100)
        self.first_name_entry.pack(pady=5)

        # last name
        self.last_name_label = tk.Label(
            self.root, text="Please enter the last name", font=("Arial", 12)
        )
        self.last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, width=100)
        self.last_name_entry.pack(pady=5)

        # submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.roles_option.get()
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

        if len(errors) == 0:
            user = self.user_manager.create_user(username, password, role)
            if user is not None:
                profile = self.profile_manager.create_profile(
                    first_name, last_name, user.id
                )
                if profile is not None:
                    messagebox.showinfo("Information", "User has been created.")
        else:
            messages = "\n".join(errors)
            messagebox.showinfo("Information", messages)


class DeleteUserForm(BaseForm):
    config: Config = None

    def __init__(self, root, config, view_users_callback):
        super().__init__(root)
        DeleteUserForm.config = config
        self.user_manager = UserManager(config)
        self.view_users_callback = view_users_callback

    def show_form(self):
        self.clear_screen()
        # return button
        self.return_button = tk.Button(
            self.root, text="Return", command=self.view_users_callback
        )
        self.return_button.pack(pady=20)

        options = []
        for user in self.user_manager.get_users():
            options.append(user.username)

        self.roles_option = ttk.Combobox(self.root, values=options)
        self.roles_option.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def submit(self):
        form_user = self.roles_option.get()
        deleted_user = self.user_manager.get_user(form_user)
        self.user_manager.delete_user(deleted_user)
        messagebox.showinfo("Information", "User has been deleted.")


class UpdateUserForm(BaseForm):
    config: Config = None

    def __init__(self, root, config, view_users_callback):
        super().__init__(root)
        UpdateUserForm.config = config
        self.user_manager = UserManager(config)
        self.profile_manager = ProfileManager(config)
        self.view_users_callback = view_users_callback

    def show_form(self, username):
        self.clear_screen()
        # return button
        self.return_button = tk.Button(
            self.root, text="Return", command=self.view_users_callback
        )
        self.return_button.pack(pady=20)

        title_label = tk.Label(
            self.root, text="Update user", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        updated_user = self.user_manager.get_user(username)
        updated_profile = self.profile_manager.get_profile(updated_user.id)

        # username
        self.current_username_label = tk.Label(
            self.root, text="Current Username", font=("Arial", 12)
        )
        self.current_username_label.pack(pady=5)
        self.current_username_entry = tk.Entry(self.root, width=100)
        self.current_username_entry.insert(0, updated_user.username)
        self.current_username_entry.config(state="readonly")
        self.current_username_entry.pack(pady=5)

        # role
        self.current_role_label = tk.Label(
            self.root, text="Current Role", font=("Arial", 12)
        )
        self.current_role_label.pack(pady=5)
        self.current_role_entry = tk.Entry(self.root, width=100)
        self.current_role_entry.insert(0, updated_user.role)
        self.current_role_entry.config(state="readonly")
        self.current_role_entry.pack(pady=5)

        self.username_label = tk.Label(self.root, text="Username", font=("Arial", 12))
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=100)
        self.username_entry.insert(0, updated_user.username)
        self.username_entry.pack(pady=5)

        # password
        self.password_label = tk.Label(
            self.root, text="Please enter the new password", font=("Arial", 12)
        )
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=100)
        self.password_entry.pack(pady=5)

        # role
        self.role_label = tk.Label(
            self.root, text="Select an role:", width=100, font=("Arial", 12)
        )
        self.role_label.pack(pady=10)
        options = [User.Role.CONSULTANT.value, User.Role.SYSTEM_ADMIN.value]
        self.roles_option = ttk.Combobox(self.root, values=options)
        self.roles_option.pack()

        # first name
        self.first_name_label = tk.Label(
            self.root, text="Please enter the first name", font=("Arial", 12)
        )
        self.first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, width=100)
        self.first_name_entry.insert(0, updated_profile.first_name)
        self.first_name_entry.pack(pady=5)

        # last name
        self.last_name_label = tk.Label(
            self.root, text="Please enter the last name", font=("Arial", 12)
        )
        self.last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, width=100)
        self.last_name_entry.insert(0, updated_profile.last_name)
        self.last_name_entry.pack(pady=5)

        # submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def submit(self):
        current_username = self.current_username_entry.get()
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()
        new_role = self.roles_option.get()
        new_first_name = self.first_name_entry.get()
        new_last_name = self.last_name_entry.get()

        try:
            user_to_update = self.user_manager.get_user(current_username)
            if user_to_update is not None:

                errors = []
                if not validate_username(new_username):
                    errors.append("Username is not valid.")

                if not validate_password(new_password):
                    errors.append("Password is not valid.")

                if not validate_name(new_first_name):
                    errors.append("First name has to be between 2 and 20 characters.")

                if not validate_name(new_last_name):
                    errors.append("Last name has to be between 2 and 20 characters.")

                if len(errors) == 0:
                    self.user_manager.update_user(
                        user_to_update, new_username, new_password, new_role
                    )
                    updated_user = self.user_manager.get_user(new_username)
                    if updated_user is not None:
                        messagebox.showinfo(
                            "Information", "User has been updated successfully."
                        )
                    else:
                        messagebox.showerror(
                            "Error", "Failed to retrieve updated user."
                        )
                else:
                    messages = "\n".join(errors)
                    messagebox.showinfo("Information", messages)
            else:
                messagebox.showerror("Error", "User not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")


# Members
class CreateMemberForm(BaseForm):
    config: Config = None

    def __init__(self, root, config, view_members_callback):
        super().__init__(root)
        CreateMemberForm.config = config
        self.member_manager = MemberManager(config)
        self.address_manager = AddressManager(config)
        self.view_members_callback = view_members_callback

    def show_form(self):
        self.clear_screen()
        # Create a title label
        title_label = tk.Label(
            self.root, text="Create new member", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # return button
        self.return_button = tk.Button(
            self.root, text="Return", command=self.view_members_callback
        )
        self.return_button.pack(pady=20)

        # first name
        self.first_name_label = tk.Label(
            self.root, text="Please enter the first name", font=("Arial", 12)
        )
        self.first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, width=100)
        self.first_name_entry.pack(pady=5)

        # last name
        self.last_name_label = tk.Label(
            self.root, text="Please enter the last name", font=("Arial", 12)
        )
        self.last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, width=100)
        self.last_name_entry.pack(pady=5)

        # age
        self.age_label = tk.Label(
            self.root, text="Please enter the age", font=("Arial", 12)
        )
        self.age_label.pack(pady=5)
        self.age_entry = tk.Entry(self.root, width=100)
        self.age_entry.pack(pady=5)

        # gender
        self.gender_label = tk.Label(
            self.root, text="Select a gender:", width=100, font=("Arial", 12)
        )
        self.gender_label.pack(pady=10)
        options = [Member.Gender.MALE.value, Member.Gender.FEMALE.value]
        self.genders_option = ttk.Combobox(self.root, values=options)
        self.genders_option.pack()

        # weight
        self.weight_label = tk.Label(
            self.root, text="Please enter the weight", font=("Arial", 12)
        )
        self.weight_label.pack(pady=5)
        self.weight_entry = tk.Entry(self.root, width=100)
        self.weight_entry.pack(pady=5)

        # email
        self.email_label = tk.Label(
            self.root, text="Please enter the email", font=("Arial", 12)
        )
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=100)
        self.email_entry.pack(pady=5)

        # phone number
        self.phone_number_label = tk.Label(
            self.root, text="Please enter the phone number", font=("Arial", 12)
        )
        self.phone_number_label.pack(pady=5)
        self.phone_number_entry = tk.Entry(self.root, width=100)
        self.phone_number_entry.pack(pady=5)

        # DIVIDER
        divider = tk.Label(self.root, text="---------------------------------")
        divider.pack(pady=5)

        # address: street
        self.street_label = tk.Label(
            self.root, text="Please enter the street", font=("Arial", 12)
        )
        self.street_label.pack(pady=5)
        self.street_entry = tk.Entry(self.root, width=100)
        self.street_entry.pack(pady=5)

        # address: house number
        self.house_number_label = tk.Label(
            self.root, text="Please enter the house number", font=("Arial", 12)
        )
        self.house_number_label.pack(pady=5)
        self.house_number_entry = tk.Entry(self.root, width=100)
        self.house_number_entry.pack(pady=5)

        # address: zip code
        self.zip_code_label = tk.Label(
            self.root, text="Please enter the zip code", font=("Arial", 12)
        )
        self.zip_code_label.pack(pady=5)
        self.zip_code_entry = tk.Entry(self.root, width=100)
        self.zip_code_entry.pack(pady=5)

        # address: city
        self.city_label = tk.Label(
            self.root, text="Select a city:", width=100, font=("Arial", 12)
        )
        self.city_label.pack(pady=10)
        city_options = [city.value for city in Address.City]
        self.city_option = ttk.Combobox(self.root, values=city_options)
        self.city_option.pack()

        # submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def submit(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        age = self.age_entry.get()
        gender = self.genders_option.get()
        weight = self.weight_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        street = self.street_entry.get()
        house_number = self.house_number_entry.get()
        zip_code = self.zip_code_entry.get()
        city = self.city_option.get()

        errors = []
        if not validate_name(first_name):
            errors.append("First name has to be between 2 and 20 characters.")

        if not validate_name(last_name):
            errors.append("Last name has to be between 2 and 20 characters.")

        if not validate_age(age):
            errors.append("Age has to be between 1 and 100.")

        if not validate_weight(weight):
            errors.append("Weight has to be between 1 and 200.")

        if not validate_email(email):
            errors.append("Email is not valid.")

        if not validate_phone_number(phone_number):
            errors.append("Phone number is not valid.")

        if not validate_street_name(street):
            errors.append("Street name has to be between 2 and 30 characters.")

        if not validate_house_number(house_number):
            errors.append("House number has to be between 1 and 9999.")

        if not validate_zip_code(zip_code):
            errors.append("Zip code is not valid.")

        if len(errors) == 0:
            member = self.member_manager.create_member(
                first_name, last_name, age, gender, weight, email, phone_number
            )
            if member is not None:
                address = self.address_manager.create_address(
                    street, house_number, zip_code, city, member.id
                )
                if address is not None:
                    messagebox.showinfo("Information", "Member has been created.")
        else:
            messages = "\n".join(errors)
            messagebox.showinfo("Information", messages)


class DeleteMemberForm(BaseForm):
    config: Config = None

    def __init__(self, root, config, view_members_callback):
        super().__init__(root)
        DeleteMemberForm.config = config
        self.member_manager = MemberManager(config)
        self.view_members_callback = view_members_callback

    def show_form(self):
        self.clear_screen()
        # return button
        self.return_button = tk.Button(
            self.root, text="Return", command=self.view_members_callback
        )
        self.return_button.pack(pady=20)

        options = []
        for member in self.member_manager.get_members():
            options.append(f"({member.id}) {member.first_name} {member.last_name}")

        self.members_option = ttk.Combobox(self.root, values=options)
        self.members_option.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def submit(self):
        form_member = self.members_option.get()
        member_id = int(form_member.split(")")[0].replace("(", ""))
        deleted_member = self.member_manager.get_member(member_id)
        self.member_manager.delete_member(deleted_member)
        messagebox.showinfo("Information", "Member has been deleted.")


class UpdateMemberForm(BaseForm):
    config: Config = None

    def __init__(self, root, config, view_members_callback):
        super().__init__(root)
        UpdateMemberForm.config = config
        self.member_manager = MemberManager(config)
        self.address_manager = AddressManager(config)
        self.view_members_callback = view_members_callback

    def show_form(self, member_id):
        self.clear_screen()
        # return button
        self.return_button = tk.Button(
            self.root, text="Return", command=self.view_members_callback
        )
        self.return_button.pack(pady=20)

        title_label = tk.Label(
            self.root, text="Update member", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        self.member_to_update = self.member_manager.get_member(member_id)
        self.address_to_update = self.address_manager.get_address(member_id)

        updated_member = self.member_to_update
        updated_address = self.address_to_update

        # first name
        self.updated_first_name_label = tk.Label(
            self.root, text="First Name", font=("Arial", 12)
        )
        self.updated_first_name_label.pack(pady=5)
        self.updated_first_name_entry = tk.Entry(self.root, width=100)
        self.updated_first_name_entry.insert(0, updated_member.first_name)
        self.updated_first_name_entry.pack(pady=5)

        # last name
        self.updated_last_name_label = tk.Label(
            self.root, text="Last Name", font=("Arial", 12)
        )
        self.updated_last_name_label.pack(pady=5)
        self.updated_last_name_entry = tk.Entry(self.root, width=100)
        self.updated_last_name_entry.insert(0, updated_member.last_name)
        self.updated_last_name_entry.pack(pady=5)

        # age
        self.updated_age_label = tk.Label(self.root, text="New Age", font=("Arial", 12))
        self.updated_age_label.pack(pady=5)
        self.updated_age_entry = tk.Entry(self.root, width=100)
        self.updated_age_entry.insert(0, updated_member.age)
        self.updated_age_entry.pack(pady=5)

        # gender
        self.gender_label = tk.Label(
            self.root, text="Select a gender:", width=100, font=("Arial", 12)
        )
        self.gender_label.pack(pady=10)
        options = [Member.Gender.MALE.value, Member.Gender.FEMALE.value]
        self.genders_option = ttk.Combobox(self.root, values=options)
        self.genders_option.insert(0, updated_member.gender)
        self.genders_option.pack()

        # weight
        self.updated_weight_label = tk.Label(
            self.root, text="New Weight", font=("Arial", 12)
        )
        self.updated_weight_label.pack(pady=5)
        self.updated_weight_entry = tk.Entry(self.root, width=100)
        self.updated_weight_entry.insert(0, updated_member.weight)
        self.updated_weight_entry.pack(pady=5)

        # email
        self.updated_email_label = tk.Label(
            self.root, text="New Email", font=("Arial", 12)
        )
        self.updated_email_label.pack(pady=5)
        self.updated_email_entry = tk.Entry(self.root, width=100)
        self.updated_email_entry.insert(0, updated_member.email)
        self.updated_email_entry.pack(pady=5)

        # phone number
        self.updated_phone_number_label = tk.Label(
            self.root, text="New Phone Number", font=("Arial", 12)
        )
        self.updated_phone_number_label.pack(pady=5)
        self.updated_phone_number_entry = tk.Entry(self.root, width=100)
        self.updated_phone_number_entry.insert(0, updated_member.phone_number)
        self.updated_phone_number_entry.pack(pady=5)

        # DIVIDER
        divider = tk.Label(self.root, text="---------------------------------")
        divider.pack(pady=5)

        # address: street
        self.street_label = tk.Label(
            self.root, text="Please enter the street", font=("Arial", 12)
        )
        self.street_label.pack(pady=5)
        self.street_entry = tk.Entry(self.root, width=100)
        self.street_entry.pack(pady=5)
        self.street_entry.insert(0, updated_address.street_name)

        # address: house number
        self.house_number_label = tk.Label(
            self.root, text="Please enter the house number", font=("Arial", 12)
        )
        self.house_number_label.pack(pady=5)
        self.house_number_entry = tk.Entry(self.root, width=100)
        self.house_number_entry.pack(pady=5)
        self.house_number_entry.insert(0, updated_address.house_number)

        # address: zip code
        self.zip_code_label = tk.Label(
            self.root, text="Please enter the zip code", font=("Arial", 12)
        )
        self.zip_code_label.pack(pady=5)
        self.zip_code_entry = tk.Entry(self.root, width=100)
        self.zip_code_entry.pack(pady=5)
        self.zip_code_entry.insert(0, updated_address.zip_code)

        # address: city
        self.city_label = tk.Label(
            self.root, text="Select a city:", width=100, font=("Arial", 12)
        )
        self.city_label.pack(pady=10)
        city_options = [city.value for city in Address.City]
        self.city_option = ttk.Combobox(self.root, values=city_options)
        self.city_option.pack()
        self.city_option.insert(0, updated_address.city)

        # submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

    def submit(self):
        updated_first_name = self.updated_first_name_entry.get()
        updated_last_name = self.updated_last_name_entry.get()
        updated_age = self.updated_age_entry.get()
        updated_gender = self.genders_option.get()
        updated_weight = self.updated_weight_entry.get()
        updated_email = self.updated_email_entry.get()
        updated_phone_number = self.updated_phone_number_entry.get()
        updated_street = self.street_entry.get()
        updated_house_number = self.house_number_entry.get()
        updated_zip_code = self.zip_code_entry.get()
        updated_city = self.city_option.get()

        errors = []
        if not validate_name(updated_first_name):
            errors.append("First name has to be between 2 and 20 characters.")

        if not validate_name(updated_last_name):
            errors.append("Last name has to be between 2 and 20 characters.")

        if not validate_age(updated_age):
            errors.append("Age has to be between 1 and 100.")

        if not validate_weight(updated_weight):
            errors.append("Weight has to be between 1 and 200.")

        if not validate_email(updated_email):
            errors.append("Email is not valid.")

        if not validate_phone_number(updated_phone_number):
            errors.append("Phone number is not valid.")

        if not validate_street_name(updated_street):
            errors.append("Street name has to be between 2 and 30 characters.")

        if not validate_house_number(updated_house_number):
            errors.append("House number has to be between 1 and 9999.")

        if not validate_zip_code(updated_zip_code):
            errors.append("Zip code is not valid.")

        if len(errors) == 0:
            member_to_update = self.member_to_update
            self.member_manager.update_member(
                member_to_update,
                updated_first_name,
                updated_last_name,
                updated_age,
                updated_gender,
                updated_weight,
                updated_email,
                updated_phone_number,
            )
            updated_member = self.member_manager.get_member(member_to_update.id)
            if updated_member is not None:
                address_to_update = self.address_to_update
                self.address_manager.update_address(
                    address_to_update,
                    updated_street,
                    updated_house_number,
                    updated_zip_code,
                    updated_city,
                    member_to_update.id,
                )
                updated_address = self.address_manager.get_address(member_to_update.id)
                if updated_address is not None:
                    messagebox.showinfo(
                        "Information", "Member has been updated successfully."
                    )
                else:
                    messagebox.showerror("Error", "Failed to retrieve updated address.")
            else:
                messagebox.showerror("Error", "Failed to retrieve updated member.")
        else:
            messages = "\n".join(errors)
            messagebox.showinfo("Information", messages)
