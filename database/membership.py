CREATE_MEMBERSHIP_TABLE = """
				CREATE TABLE IF NOT EXISTS membership (
				id INTEGER PRIMARY KEY,
				member_user_id INTEGER,
				FOREIGN KEY(member_user_id) REFERENCES user(user_id) ON DELETE CASCADE

				);
			"""


def initialize_membership_table(con):
    cursor = con.cursor()
    cursor.execute(CREATE_MEMBERSHIP_TABLE)
    con.commit()
