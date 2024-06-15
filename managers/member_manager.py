from config import Config
from entities.address import Address
from utils import (
    rsa_encrypt,
    rsa_decrypt,
    generate_registration_date,
    generate_membership_id,
)
from managers.base_manager import BaseManager
from entities.member import Member


class MemberManager(BaseManager):
    def __init__(self, config: Config):
        super().__init__(config)

    def initialize(self):
        SQL_CREATE_MEMBER_TABLE = """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                weight INTEGER NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                registration_date TEXT NOT NULL,
                membership_id INTEGER NOT NULL
            );
        """

        try:
            cursor = self.config.con.cursor()
            cursor.execute(SQL_CREATE_MEMBER_TABLE)
            self.config.con.commit()
        finally:
            cursor.close()

    def get_members(self) -> list[Member]:
        SQL_SELECT_MEMBERS = "SELECT * FROM members;"
        try:
            cursor = self.config.con.cursor()
            cursor.execute(SQL_SELECT_MEMBERS)
            result = cursor.fetchall()
        finally:
            cursor.close()

        members = []
        for member_data in result:
            member = Member(*member_data)
            member.first_name = rsa_decrypt(member.first_name, self.config.private_key)
            member.last_name = rsa_decrypt(member.last_name, self.config.private_key)
            member.age = rsa_decrypt(member.age, self.config.private_key)
            member.gender = rsa_decrypt(member.gender, self.config.private_key)
            member.weight = rsa_decrypt(member.weight, self.config.private_key)
            member.email = rsa_decrypt(member.email, self.config.private_key)
            member.phone_number = rsa_decrypt(
                member.phone_number, self.config.private_key
            )
            member.registration_date = rsa_decrypt(
                member.registration_date, self.config.private_key
            )
            member.membership_id = rsa_decrypt(
                member.membership_id, self.config.private_key
            )
            members.append(member)

        return members

    def get_member(self, id: int) -> Member:
        for member in self.get_members():
            if member.id == id:
                return member
        return None

    def create_member(
        self,
        first_name: str,
        last_name: str,
        age: int,
        gender: str,
        weight: int,
        email: str,
        phone_number: str,
    ) -> Member:
        registration_date = generate_registration_date()
        encrypted_first_name = rsa_encrypt(first_name, self.config.public_key)
        encrypted_last_name = rsa_encrypt(last_name, self.config.public_key)
        encrypted_age = rsa_encrypt(age, self.config.public_key)
        encrypted_gender = rsa_encrypt(gender, self.config.public_key)
        encrypted_weight = rsa_encrypt(weight, self.config.public_key)
        encrypted_email = rsa_encrypt(email, self.config.public_key)
        encrypted_phone_number = rsa_encrypt(phone_number, self.config.public_key)
        encrypted_registration_date = rsa_encrypt(
            registration_date, self.config.public_key
        )
        encrypted_membership_id = rsa_encrypt(
            generate_membership_id(registration_date), self.config.public_key
        )

        SQL_CREATE_MEMBER = """
            INSERT INTO members (
                first_name,
                last_name,
                age,
                gender,
                weight,
                email,
                phone_number,
                registration_date,
                membership_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        try:
            cursor = self.config.con.cursor()
            cursor.execute(
                SQL_CREATE_MEMBER,
                (
                    encrypted_first_name,
                    encrypted_last_name,
                    encrypted_age,
                    encrypted_gender,
                    encrypted_weight,
                    encrypted_email,
                    encrypted_phone_number,
                    encrypted_registration_date,
                    encrypted_membership_id,
                ),
            )
            self.config.con.commit()
        finally:
            cursor.close()

        return self.get_member(cursor.lastrowid)

    def update_member(
        self,
        member: Member,
        first_name: str,
        last_name: str,
        age: int,
        gender: str,
        weight: int,
        email: str,
        phone_number: str,
    ) -> Member:
        encrypted_first_name = rsa_encrypt(first_name, self.config.public_key)
        encrypted_last_name = rsa_encrypt(last_name, self.config.public_key)
        encrypted_age = rsa_encrypt(age, self.config.public_key)
        encrypted_gender = rsa_encrypt(gender, self.config.public_key)
        encrypted_weight = rsa_encrypt(weight, self.config.public_key)
        encrypted_email = rsa_encrypt(email, self.config.public_key)
        encrypted_phone_number = rsa_encrypt(phone_number, self.config.public_key)

        SQL_UPDATE_MEMBER = """
            UPDATE members SET
                first_name = ?,
                last_name = ?,
                age = ?,
                gender = ?,
                weight = ?,
                email = ?,
                phone_number = ?
            WHERE id = ?;
        """

        try:
            cursor = self.config.con.cursor()
            cursor.execute(
                SQL_UPDATE_MEMBER,
                (
                    encrypted_first_name,
                    encrypted_last_name,
                    encrypted_age,
                    encrypted_gender,
                    encrypted_weight,
                    encrypted_email,
                    encrypted_phone_number,
                    member.id,
                ),
            )
            self.config.con.commit()
        finally:
            cursor.close()

        return self.get_member(member.id)

    def delete_member(self, member: Member):
        SQL_DELETE_MEMBER = """
            DELETE FROM members WHERE id = ?;
        """

        try:
            cursor = self.config.con.cursor()
            cursor.execute(SQL_DELETE_MEMBER, (member.id,))
            self.config.con.commit()
        finally:
            cursor.close()
