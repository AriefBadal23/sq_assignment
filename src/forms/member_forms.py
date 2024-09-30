import tkinter as tk
from tkinter import ttk
from entities.member import Member
from entities.address import Address
from tkinter import messagebox
from managers.member_manager import MemberManager
from managers.address_manager import AddressManager
from entities.user import User
from validations import (
    validate_name,
    validate_age,
    validate_server_input,
    validate_weight,
    validate_email,
    validate_phone_number,
    validate_street_name,
    validate_house_number,
    validate_zip_code,
)
from forms.base_form import BaseForm


class CreateMemberForm(BaseForm):
    def __init__(
        self,
        root,
        config,
        logger,
        sender,
        authorize,
        view_members_callback,
    ):
        authorized_roles = (
            User.Role.SUPER_ADMIN,
            User.Role.SYSTEM_ADMIN,
            User.Role.CONSULTANT,
        )
        super().__init__(root, config, logger, sender, authorize, authorized_roles)
        self.member_manager = MemberManager(self.config)
        self.address_manager = AddressManager(self.config)
        self.view_members_callback = view_members_callback

    def show_form(self):
        self.authorize(self.authorized_roles)

        self.clear_screen()
        # Create a title label
        title_label = tk.Label(
            self.root, text="Create new member", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

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

        # age
        self.age_label = tk.Label(
            self.root, text="Please enter the age", font=("Arial", 12)
        )
        self.age_label.pack(pady=5, padx=25)
        self.age_entry = tk.Entry(self.root, width=100)
        self.age_entry.pack(pady=5, padx=25)

        # gender
        self.gender_label = tk.Label(
            self.root, text="Select a gender:", width=100, font=("Arial", 12)
        )
        self.gender_label.pack(pady=10)
        self.gender_options = [Member.Gender.MALE.value, Member.Gender.FEMALE.value]
        self.genders_option = ttk.Combobox(self.root, values=self.gender_options)
        self.genders_option.pack()

        # weight
        self.weight_label = tk.Label(
            self.root, text="Please enter the weight", font=("Arial", 12)
        )
        self.weight_label.pack(pady=5, padx=25)
        self.weight_entry = tk.Entry(self.root, width=100)
        self.weight_entry.pack(pady=5, padx=25)

        # email
        self.email_label = tk.Label(
            self.root, text="Please enter the email", font=("Arial", 12)
        )
        self.email_label.pack(pady=5, padx=25)
        self.email_entry = tk.Entry(self.root, width=100)
        self.email_entry.pack(pady=5, padx=25)

        # phone number
        self.phone_number_label = tk.Label(
            self.root, text="Please enter the phone number", font=("Arial", 12)
        )
        self.phone_number_label.pack(pady=5, padx=25)
        self.phone_number_entry = tk.Entry(self.root, width=100)
        self.phone_number_entry.pack(pady=5, padx=25)

        # DIVIDER
        divider = tk.Label(self.root, text="---------------------------------")
        divider.pack(pady=5, padx=25)

        # address: street
        self.street_label = tk.Label(
            self.root, text="Please enter the street", font=("Arial", 12)
        )
        self.street_label.pack(pady=5, padx=25)
        self.street_entry = tk.Entry(self.root, width=100)
        self.street_entry.pack(pady=5, padx=25)

        # address: house number
        self.house_number_label = tk.Label(
            self.root, text="Please enter the house number", font=("Arial", 12)
        )
        self.house_number_label.pack(pady=5, padx=25)
        self.house_number_entry = tk.Entry(self.root, width=100)
        self.house_number_entry.pack(pady=5, padx=25)

        # address: zip code
        self.zip_code_label = tk.Label(
            self.root, text="Please enter the zip code", font=("Arial", 12)
        )
        self.zip_code_label.pack(pady=5, padx=25)
        self.zip_code_entry = tk.Entry(self.root, width=100)
        self.zip_code_entry.pack(pady=5, padx=25)

        # address: city
        self.city_label = tk.Label(
            self.root, text="Select a city:", width=100, font=("Arial", 12)
        )
        self.city_label.pack(pady=10)
        self.city_options = [city.value for city in Address.City]
        self.city_option = ttk.Combobox(self.root, values=self.city_options)
        self.city_option.pack()

        # submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

        # back button
        self.back_button = tk.Button(
            self.root, text="Cancel", command=self.view_members_callback
        )
        self.back_button.pack(pady=20)

    def submit(self):
        self.authorize(self.authorized_roles)

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

        if not validate_server_input(gender, self.gender_options):
            errors.append("Gender is not valid, incident will be reported.")
            self.logger.log_activity(
                self.sender,
                "Server-side input is modified.",
                f"Gender was not valid: {gender}",
                True,
            )

        if not validate_server_input(city, self.city_options):
            errors.append("City is not valid, incident will be reported.")
            self.logger.log_activity(
                self.sender,
                "Server-side input is modified.",
                f"City was not valid: {city}",
                True,
            )

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
                    self.logger.log_activity(
                        self.sender, "created member", f"with id: {member.id}", False
                    )
                    self.view_members_callback()
        else:
            messages = "\n".join(errors)
            messagebox.showinfo("Information", messages)


class UpdateMemberForm(BaseForm):
    def __init__(
        self,
        root,
        config,
        logger,
        sender,
        authorize,
        view_members_callback,
    ):
        authorized_roles = (
            User.Role.SUPER_ADMIN,
            User.Role.SYSTEM_ADMIN,
            User.Role.CONSULTANT,
        )
        super().__init__(root, config, logger, sender, authorize, authorized_roles)
        self.member_manager = MemberManager(config)
        self.address_manager = AddressManager(config)
        self.view_members_callback = view_members_callback

    def show_form(self, member_id):
        self.authorize(self.authorized_roles)

        self.clear_screen()

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
        self.updated_first_name_label.pack(pady=5, padx=25)
        self.updated_first_name_entry = tk.Entry(self.root, width=100)
        self.updated_first_name_entry.insert(0, updated_member.first_name)
        self.updated_first_name_entry.pack(pady=5, padx=25)

        # last name
        self.updated_last_name_label = tk.Label(
            self.root, text="Last Name", font=("Arial", 12)
        )
        self.updated_last_name_label.pack(pady=5, padx=25)
        self.updated_last_name_entry = tk.Entry(self.root, width=100)
        self.updated_last_name_entry.insert(0, updated_member.last_name)
        self.updated_last_name_entry.pack(pady=5, padx=25)

        # age
        self.updated_age_label = tk.Label(self.root, text="New Age", font=("Arial", 12))
        self.updated_age_label.pack(pady=5, padx=25)
        self.updated_age_entry = tk.Entry(self.root, width=100)
        self.updated_age_entry.insert(0, updated_member.age)
        self.updated_age_entry.pack(pady=5, padx=25)

        # gender
        self.gender_label = tk.Label(
            self.root, text="Select a gender:", width=100, font=("Arial", 12)
        )
        self.gender_label.pack(pady=10)
        self.gender_options = [Member.Gender.MALE.value, Member.Gender.FEMALE.value]
        self.genders_option = ttk.Combobox(self.root, values=self.gender_options)
        self.genders_option.insert(0, updated_member.gender)
        self.genders_option.pack()

        # weight
        self.updated_weight_label = tk.Label(
            self.root, text="New Weight", font=("Arial", 12)
        )
        self.updated_weight_label.pack(pady=5, padx=25)
        self.updated_weight_entry = tk.Entry(self.root, width=100)
        self.updated_weight_entry.insert(0, updated_member.weight)
        self.updated_weight_entry.pack(pady=5, padx=25)

        # email
        self.updated_email_label = tk.Label(
            self.root, text="New Email", font=("Arial", 12)
        )
        self.updated_email_label.pack(pady=5, padx=25)
        self.updated_email_entry = tk.Entry(self.root, width=100)
        self.updated_email_entry.insert(0, updated_member.email)
        self.updated_email_entry.pack(pady=5, padx=25)

        # phone number
        self.updated_phone_number_label = tk.Label(
            self.root, text="New Phone Number", font=("Arial", 12)
        )
        self.updated_phone_number_label.pack(pady=5, padx=25)
        self.updated_phone_number_entry = tk.Entry(self.root, width=100)
        self.updated_phone_number_entry.insert(0, updated_member.phone_number)
        self.updated_phone_number_entry.pack(pady=5, padx=25)

        # DIVIDER
        divider = tk.Label(self.root, text="---------------------------------")
        divider.pack(pady=5, padx=25)

        # address: street
        self.street_label = tk.Label(
            self.root, text="Please enter the street", font=("Arial", 12)
        )
        self.street_label.pack(pady=5, padx=25)
        self.street_entry = tk.Entry(self.root, width=100)
        self.street_entry.pack(pady=5, padx=25)
        self.street_entry.insert(0, updated_address.street_name)

        # address: house number
        self.house_number_label = tk.Label(
            self.root, text="Please enter the house number", font=("Arial", 12)
        )
        self.house_number_label.pack(pady=5, padx=25)
        self.house_number_entry = tk.Entry(self.root, width=100)
        self.house_number_entry.pack(pady=5, padx=25)
        self.house_number_entry.insert(0, updated_address.house_number)

        # address: zip code
        self.zip_code_label = tk.Label(
            self.root, text="Please enter the zip code", font=("Arial", 12)
        )
        self.zip_code_label.pack(pady=5, padx=25)
        self.zip_code_entry = tk.Entry(self.root, width=100)
        self.zip_code_entry.pack(pady=5, padx=25)
        self.zip_code_entry.insert(0, updated_address.zip_code)

        # address: city
        self.city_label = tk.Label(
            self.root, text="Select a city:", width=100, font=("Arial", 12)
        )
        self.city_label.pack(pady=10)
        self.city_options = [city.value for city in Address.City]
        self.city_option = ttk.Combobox(self.root, values=self.city_options)
        self.city_option.pack()
        self.city_option.insert(0, updated_address.city)

        # submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

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
            self.root, text="Cancel", command=self.view_members_callback
        )
        self.back_button.pack(pady=5)

    def submit(self):
        self.authorize(self.authorized_roles)

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

        if not validate_server_input(updated_gender, self.gender_options):
            errors.append("Gender is not valid, incident will be reported.")
            self.logger.log_activity(
                self.sender,
                "Server-side input is modified.",
                f"Gender was not valid: {updated_gender}",
                True,
            )

        if not validate_server_input(updated_city, self.city_options):
            errors.append("City is not valid, incident will be reported.")
            self.logger.log_activity(
                self.sender,
                "Server-side input is modified.",
                f"City was not valid: {updated_city}",
                True,
            )

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
                    self.logger.log_activity(
                        self.sender,
                        "updated member",
                        f"with id: {updated_member.id}",
                        False,
                    )
                    self.view_members_callback()
                else:
                    messagebox.showerror("Error", "Failed to retrieve updated address.")
            else:
                messagebox.showerror("Error", "Failed to retrieve updated member.")
        else:
            messages = "\n".join(errors)
            messagebox.showinfo("Information", messages)

    def delete(self):
        self.authorize(self.authorized_roles)

        member = self.member_manager.get_member(self.member_to_update.id)
        self.member_manager.delete_member(member)
        messagebox.showinfo("Information", "Member has been deleted.")
        self.logger.log_activity(
            self.sender, "deleted member", f"with id: {member.id}", False
        )
        self.view_members_callback()
