from entities.address import Address


class AddressManager:
    def __init__(self, con):
        self.con = con

    @staticmethod
    def initialize(con):
        SQL_CREATE_ADDRESS_TABLE = """
            CREATE TABLE IF NOT EXISTS addresses (
                address_id INTEGER PRIMARY KEY,
                street_name TEXT NOT NULL,
                house_number TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                city TEXT NOT NULL
            );
        """

        SQL_CREATE_USER_ADDRESS_TABLE = """
            CREATE TABLE IF NOT EXISTS user_addresses (
                user_id INTEGER,
                address_id INTEGER,
                PRIMARY KEY (user_id, address_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (address_id) REFERENCES address(address_id)
            );
        """

        cursor = con.cursor()
        cursor.execute(SQL_CREATE_ADDRESS_TABLE)
        cursor.execute(SQL_CREATE_USER_ADDRESS_TABLE)
        con.commit()
        cursor.close()
