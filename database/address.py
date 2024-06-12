CREATE_ADDRESS_TABLE = """
				CREATE TABLE IF NOT EXISTS address (
				address_id INTEGER PRIMARY KEY,
				streetname TEXT NOT NULL,
				house_number INTEGER NOT NULL,
				zipcode INTEGER NOT NULL,
				city TEXT NOT NULL

				);
			"""

CREATE_USER_ADDRESS_TABLE = """
				CREATE TABLE IF NOT EXISTS user_address (
				user_Id INTEGER,
				address_Id INTEGER,
				PRIMARY KEY (user_id, address_id),
				FOREIGN KEY (user_Id) REFERENCES user(user_id)
				FOREIGN KEY (address_Id) REFERENCES address(address_id)
				);
			"""


def initialize_user_address_table(con):
    cursor = con.cursor()
    cursor.execute(CREATE_USER_ADDRESS_TABLE)
    con.commit()
    
def initialize_address_table(con):
    cursor = con.cursor()
    cursor.execute(CREATE_ADDRESS_TABLE)
    con.commit()
