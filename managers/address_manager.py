from config import Config
from managers.base_manager import BaseManager
from entities.address import Address


class AddressManager(BaseManager):
    def __init__(self, config: Config):
        super().__init__(config)

    def initialize(self):
        SQL_CREATE_ADDRESS_TABLE = """
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY,
                street_name TEXT NOT NULL,
                house_number TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                city TEXT NOT NULL,
                member_id INTEGER NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
            );
        """

        try:
            cursor = self.config.con.cursor()
            cursor.execute(SQL_CREATE_ADDRESS_TABLE)
            self.config.con.commit()
        finally:
            cursor.close()

    def get_addresses(self) -> list[Address]:
        SQL_SELECT_ADDRESSES = "SELECT * FROM addresses;"
        try:
            cursor = self.config.con.cursor()
            cursor.execute(SQL_SELECT_ADDRESSES)
            result = cursor.fetchall()
        finally:
            cursor.close()

        return [Address(*address_data) for address_data in result]

    def get_address(self, member_id: int) -> Address:
        SQL_SELECT_ADDRESS = "SELECT * FROM addresses WHERE member_id = ?;"
        try:
            cursor = self.config.con.cursor()
            cursor.execute(SQL_SELECT_ADDRESS, (member_id,))
            result = cursor.fetchone()
        finally:
            cursor.close()

        return Address(*result) if result is not None else None

    def create_address(
        self,
        street_name: str,
        house_number: str,
        zip_code: str,
        city: str,
        member_id: int,
    ) -> Address:
        SQL_CREATE_ADDRESS = "INSERT INTO addresses (street_name, house_number, zip_code, city, member_id) VALUES (?, ?, ?, ?, ?);"
        try:
            cursor = self.config.con.cursor()
            cursor.execute(
                SQL_CREATE_ADDRESS,
                (street_name, house_number, zip_code, city, member_id),
            )
            self.config.con.commit()
        finally:
            cursor.close()

        return self.get_address(cursor.lastrowid)

    def update_address(
        self,
        address: Address,
        street_name: str,
        house_number: str,
        zip_code: str,
        city: str,
        member_id: int,
    ):
        SQL_UPDATE_ADDRESS = "UPDATE addresses SET street_name = ?, house_number = ?, zip_code = ?, city = ? WHERE member_id = ?;"
        try:
            cursor = self.config.con.cursor()
            cursor.execute(
                SQL_UPDATE_ADDRESS,
                (street_name, house_number, zip_code, city, member_id),
            )
            self.config.con.commit()
        finally:
            cursor.close()

        return self.get_address(address.id)
