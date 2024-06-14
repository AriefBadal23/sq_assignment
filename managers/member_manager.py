from entities.member import Member


class MemberManager:
    def __init__(self, con):
        self.con = con

    @staticmethod
    def initialize(con):
        SQL_CREATE_MEMBER_TABLE = """
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                lastname TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                weight INTEGER NOT NULL,
                address_id INTEGER,
                FOREIGN KEY (address_id) REFERENCES address(address_id)
            );
        """

        cursor = con.cursor()
        cursor.execute(SQL_CREATE_MEMBER_TABLE)
        con.commit()
        cursor.close()
