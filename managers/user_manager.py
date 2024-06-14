from entities.user import User
import hashlib


class UserManager:
    @staticmethod
    def initialize(con):
        SQL_CREATE_USER_TABLE = """
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY ,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
                );
            """

        cursor = con.cursor()
        cursor.execute(SQL_CREATE_USER_TABLE)
        con.commit()
        cursor.close()

    @staticmethod
    def create_super_admin(con):
        password = UserManager.password_hash("Admin_123?")
        CREATE_SUPER_ADMIN = f"INSERT INTO users (username, password, role) VALUES ('super_admin', '{password}', '{User.Role.SUPER_ADMIN.value}');"
        cursor = con.cursor()
        cursor.execute(CREATE_SUPER_ADMIN)
        con.commit()
        cursor.close()

    @staticmethod
    def login(con, username, password):
        cursor = con.cursor()

        hashed_password = UserManager.password_hash(password)
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password),
        )
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None

        return User(*result)

    @staticmethod
    def password_hash(password):
        return hashlib.sha256(password.encode()).hexdigest()
