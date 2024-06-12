from .user import initialize_user_profile_table, initialize_user_role_table, initialize_user_table
from .address import initialize_address_table
from .membership import initialize_membership_table
from .role import intitialize_role_table,add_default_user_roles
from .user import initialize_user_table, create_super_user, create_super_profile, create_super_role
import sqlite3


# TODO: mv to config.py
def connect():
    return sqlite3.connect("data.db")


def initialize_database_tables():
    con = connect()
    intitialize_role_table(con)
    initialize_user_table(con) 
    initialize_user_role_table(con)
    initialize_address_table(con)
    initialize_user_address_table(con)
    initialize_membership_table(con)
    initialize_user_profile_table(con)
    add_default_user_roles(con)
    create_super_user(con)
    create_super_profile(con)
    create_super_role(con)
    con.close()
