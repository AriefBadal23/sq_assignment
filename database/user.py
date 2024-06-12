import datetime
import hashlib

SQL_CREATE_USER_TABLE = """
                CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY ,
                assigned_role_id INTEGER,
                username TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                registration_date TEXT NOT NULL,
                mobile TEXT UNIQUE,
                password TEXT NOT NULL,
                FOREIGN KEY (assigned_role_id) REFERENCES role(role_id) ON DELETE CASCADE
                );
            """

CREATE_USER_ROLE_TABLE = """
                CREATE TABLE IF NOT EXISTS user_role (
                user_Id INTEGER,
                role_id INTEGER,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY (user_Id) REFERENCES user(user_id) ON DELETE CASCADE,
                FOREIGN KEY (role_Id) REFERENCES role(role_id) ON DELETE CASCADE
                );
            """

CREATE_USER_PROFILE_TABLE = """
                CREATE TABLE IF NOT EXISTS user_profile (
                profile_id INTEGER PRIMARY KEY ,
                name TEXT NOT NULL,
                lastname TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                weight INTEGER NOT NULL,
                FOREIGN KEY (profile_Id) REFERENCES user(user_id) ON DELETE CASCADE
                );
            """


CREATE_SUPER_ADMIN_ROLE = [
    "PRAGMA foreign_keys = ON;",
    "INSERT INTO user_role (user_id, role_id) VALUES (1,1);",
]

CREATE_SUPER_PROFILE = [
    "PRAGMA foreign_keys = ON;",
    "INSERT INTO user_profile (name, lastname, age, gender, weight) VALUES ('SUPER', 'USER', 20, 'male',200);",
]

password = hashlib.sha256("Admin_123?".encode()).hexdigest()
# ? registration_date in user_profile or user?
CREATE_SUPER_ADMIN = [
    "PRAGMA foreign_keys = ON;",
    f"INSERT INTO user (assigned_role_id,username,registration_date, password) VALUES (1,'super_admin', '{datetime.datetime.now()}','{password}');",

]


def initialize_user_table(con):
    cursor = con.cursor()
    cursor.execute(SQL_CREATE_USER_TABLE)
    con.commit()


def initialize_user_role_table(con):
    cursor = con.cursor()
    cursor.execute(CREATE_USER_ROLE_TABLE)
    con.commit()


def initialize_user_profile_table(con):
    cursor = con.cursor()
    cursor.execute(CREATE_USER_PROFILE_TABLE)
    con.commit()


def create_super_user(con):
    cursor = con.cursor()
    for s in CREATE_SUPER_ADMIN:
        cursor.execute(s)
    con.commit()


def create_super_profile(con):
    cursor = con.cursor()
    for s in CREATE_SUPER_PROFILE:
        cursor.execute(s)
    con.commit()


def create_super_role(con):
    cursor = con.cursor()
    for s in CREATE_SUPER_ADMIN_ROLE:
        cursor.execute(s)
    con.commit()
