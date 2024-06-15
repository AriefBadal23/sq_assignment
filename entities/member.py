from enum import Enum


class Member:
    class Gender(Enum):
        MALE = "M"
        FEMALE = "F"

    def __init__(
        self,
        id,
        first_name,
        last_name,
        age,
        gender,
        weight,
        email,
        phone_number,
        registration_date,
        membership_id,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.email = email
        self.phone_number = phone_number
        self.registration_date = registration_date
        self.membership_id = membership_id
