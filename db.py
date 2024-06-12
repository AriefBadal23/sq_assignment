import datetime
import hashlib
import sqlite3
from user import Profile, User


def authenticate_user(connection, username: str, password: str) -> tuple:
    encrypted_password = hashlib.sha256(f"{password}".encode()).hexdigest()
    user_object = connection.execute(
        f'SELECT name || " " || lastname AS fullname, user_id AS id, assigned_role_id as role_id, email,username, password, mobile, age, gender, weight FROM user INNER JOIN user_profile ON user.user_id = user_profile.profile_id WHERE username="{username}" AND password="{encrypted_password}"'
    ).fetchone()
    if user_object is not None:
        (
            fullname,
            id,
            role_id,
            email,
            username,
            password,
            mobile,
            age,
            gender,
            weight,
        ) = user_object
        new_user = Profile(
            id,
            fullname,
            role_id,
            email,
            username,
            password,
            mobile,
            age,
            gender,
            weight,
        )
        return new_user
    else:
        print("User is invalid!")
    # TODO change global Exception to custom Exception.


def get_user_by_id(connection, id):
    user_object = connection.execute(
        f'SELECT name || " " || lastname AS fullname, user_id AS id, assigned_role_id as role_id, email,username, password, mobile, age, gender, weight FROM user INNER JOIN user_profile ON user.user_id = user_profile.profile_id WHERE user_id="{id}"'
    ).fetchone()
    if user_object is not None:
        (
            fullname,
            id,
            role_id,
            email,
            username,
            password,
            mobile,
            age,
            gender,
            weight,
        ) = user_object
        new_user = Profile(
            id,
            fullname,
            role_id,
            email,
            username,
            password,
            mobile,
            age,
            gender,
            weight,
        )
        return new_user
    else:
        print("User is invalid!")
    # TODO change global Exception to custom Exception.




def create_account(
    connection,
    current_role,
    new_user_role,
    username,
    email,
    password,
    mobile,
    name,
    lastname,
    age=None,
    gender=None,
    weight=None,
):

    cursor = connection.cursor()
    statements = [
        "PRAGMA foreign_keys = ON;",
        f'INSERT INTO user(assigned_role_id,username,registration_date, email,mobile, password) VALUES({new_user_role},"{username}","{datetime.datetime.now()}","{email}","{mobile}","{password}");',
        f'INSERT INTO user_profile (name, lastname, age, gender, weight) VALUES ("{name}", "{lastname}", "{age}", "{gender}","{weight}");',
    ]

    # create admin as super
    if current_role == 1 and new_user_role == 2:        
        for statement in statements:
            cursor.execute(statement)

        id, role = cursor.execute(
            f'SELECT user_id, assigned_role_id FROM user WHERE username="{username}"'
        ).fetchone()
        cursor.execute(
            f'INSERT INTO user_role (user_id, role_id) VALUES ("{id}","{role}")'
        )
        cursor.commit()
        return cursor.lastrowid

    # create consultant as super or admin
    elif current_role == 1 or current_role == 2 and new_user_role == 3:
        for statement in statements:
            connection.execute(statement)
        connection.commit()

        id, role = connection.execute(
            f'SELECT user_id, assigned_role_id FROM user WHERE username="{username}"'
        ).fetchone()
        connection.execute(
            f'INSERT INTO user_role (user_id, role_id) VALUES ("{id}","{role}")'
        )
        connection.commit()


    # create member as super, admin or consultant
    elif current_role == 1 or current_role == 2 or current_role == 3 and new_user_role == 4:
        for statement in statements:
            connection.execute(statement)
        connection.commit()


        # TODO: make use of get_user() method
        id, role = connection.execute(
            f'SELECT user_id, assigned_role_id FROM user WHERE username="{username}"'
        ).fetchone()


        connection.execute(
            f'INSERT INTO user_role (user_id, role_id) VALUES ("{id}","{role}")'
        )
        connection.commit()
        connection.execute(
            f'INSERT INTO membership (member_user_id) VALUES ("{id}")'
        )
        connection.commit()
    else:
        # TODO: trow exception because you are not superadmin!
        return False





def update_consultant(connection, assigned_role_id, mobile):
    # TODO: update only the columns when there are new values given
    connection.execute("PRAGMA foreign_keys = ON;")
    # connection.execute(f'UPDATE user SET assigned_role_id="3",email="{email}",mobile="{mobile}",password="{password}" WHERE user_id ="2"')
    connection.execute(
        f'UPDATE user SET assigned_role_id="{assigned_role_id}",mobile="{mobile}" WHERE user_id ="2"'
    )
    connection.commit()
    print("user is updated")


def get_all_users(connection, user_id):
    users = connection.execute(
        f'SELECT name || " " || lastname AS fullname, user_id AS id, assigned_role_id as role_id, email,username, password, mobile, age, gender, weight FROM user INNER JOIN user_profile ON user.user_id = user_profile.profile_id'
    ).fetchall()
    user_objects = []
    if users != 0:
        for user in users:
            (
                fullname,
                id,
                role_id,
                email,
                username,
                password,
                mobile,
                age,
                gender,
                weight,
            ) = user
            user_profile = Profile(
                id,
                fullname,
                role_id,
                email,
                username,
                password,
                mobile,
                age,
                gender,
                weight,
            )
            if id != user_id:
                user_objects.append(user_profile)

        for u in user_objects:
            print("ID:",u.id, "|", "Role:", u.get_role() ,"|", "Email:", u.email)
            print("---------------------------------------------------------")


def delete_user(connection, role_id, user_id):
    if int(user_id) != 1 and int(role_id) == 1 or int(role_id) == 2:
        statements = [
            "PRAGMA foreign_keys = ON;",
            f'DELETE from user WHERE user_id="{user_id}"',
        ]
        for statement in statements:
            connection.execute(statement)
        connection.commit()
        print("User is deleted")
    else:
        # TODO: make try-except block
        print("Deletion has failed")


def update_password(connection, user_id, new_password):
    encrypted_password = hashlib.sha256(f"{new_password}".encode()).hexdigest()
    # TODO: update only the columns when there are new values given
    connection.execute(
        f'UPDATE user SET password="{encrypted_password}" WHERE user_id ="{user_id}"'
    )
    connection.commit()
    print("The temporary password has been updated.")


def update_user(connection,current_id,role_id, account_id, new_password, username, email, mobile, name,lastname, age, gender, weight):
    # user = get_user_by_id(connection,account_id)
    # TODO: update only the columns when there are new values given
    # ? Can the role also be updated?
    if current_id == 1 or current_id == 2:
        connection.execute(
            f'UPDATE user_profile SET name="{name}", lastname="{lastname}", age="{age}", gender="{gender}", weight="{weight}" WHERE profile_id ="{account_id}"'
        )
        connection.commit()

        connection.execute(
            f'UPDATE user SET username="{username}",  email="{email}", mobile="{mobile}", password="{new_password}", assigned_role_id="{role_id}" WHERE user_id ="{account_id}"'
        )
        connection.commit()
        print("Account is succesfully updated!")
    else:
        print("You have no authorisation to update. Only SuperAdmin, Admins and Consultants.")


    
def create_address(connection,streetname, house_number, zipcode, city):
     cursor = connection.cursor()
     cursor.execute(
            f'INSERT INTO address (streetname, house_number, zipcode, city) VALUES ("{streetname}","{house_number}", "{zipcode}","{city}")'
        )
     connection.commit()
    #  TODO: do this for the other ones as well.
     return cursor.lastrowid

    

def create_member_address(connection,user_id, streetname, house_number, zipcode, city):
    #  TODO:
     address = create_address(connection, streetname, house_number, zipcode, city)
     connection.execute(
        f'INSERT INTO user_address (user_id, address_id) VALUES ("{user_id}", "{address}")')

     connection.commit()