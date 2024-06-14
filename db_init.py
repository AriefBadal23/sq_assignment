import sqlite3
from managers.user_manager import UserManager
from managers.address_manager import AddressManager
from managers.member_manager import MemberManager


def connect():
    return sqlite3.connect("data.db")


def initialize_database_tables():
    con = connect()
    UserManager.initialize(con)
    # UserManager.create_super_admin(con)

    AddressManager.initialize(con)
    MemberManager.initialize(con)
    con.close()
