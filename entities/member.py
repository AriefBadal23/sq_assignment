from enum import Enum


class Member:
    class Gender(Enum):
        MALE = "M"
        FEMALE = "F"

    def __init__(
        self,
        first_name,
        last_name,
        age,
        gender,
        weight,
        address,
        email,
        phone_number,
        membership_type,
        membership_status,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.address = address
        self.email = email
        self.phone_number = phone_number
