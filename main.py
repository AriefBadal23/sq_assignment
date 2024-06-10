import hashlib
from database import initialize_database_tables, connect
import db


roles_menu = {
    "super_user": """
                        (1)uit, to Exit the program.
                        (2)Password reset
                        (3)Show users and roles
                        (4)update consultant
                        --------------------
                        (d)elete consultant
                        (r)eset consultant
                        (a)dd new admin
                        (c)reate consultant
                        (u)pdate admin
                        (d)elete admin
                        (r)eset admin
                        (m)ake backup
                        (rb)restore backup
                        (l)ogs
                        (n)ew member
                        (u)pdate member
                        (d)elete member
                        (f)ind member""",
    "admin": [
        ("View all users", "A"),
        ("Add new user", "B"),
        ("Generate reports", "C"),
        ("Logout", "D"),
    ],
    "consultant": [
        ("Update my password", "A"),
        ("Add new member", "B"),
        ("Update member", "C"),
        ("Search member", "C"),
    ],
}


def main():
    initialize_database_tables()
    con = connect()
    print(
        """
                    ********************************************************
                    *                                                      *
                    *          Welcome to the Member Management System     *
                    *                                                      *
                    *           Unauthorized access is prohibited          *
                    *                                                      *
                    *                  Please login to continue            *
                    *                                                      *
                    ********************************************************
    """
    )
    # username = input("Username:")
    # password = input("Password:")
    count = 0

    while True:
        username = "super_admin"
        password = "Admin_123?"

        if username and password:
            user_account = db.authenticate_user(con, username, password)
            if user_account != None:
                if user_account.role_id == 1:
                    print(roles_menu[user_account.get_role()] )
                    choice = input("Your choice: ")
                    if choice == "q":
                        print("You have been logged out")
                        break
                    elif choice == "s":
                        db.get_all_users(con, user_account.role_id)

                    elif choice == "u":
                        pass
                    elif choice == "2":
                        user_to_reset_password = input("What is the ID of the user to reset the password from?")
                        temp_password = input("Temporary password")
                        if user_to_reset_password:
                            db.update_password(con, user_to_reset_password, temp_password)
                        else:
                            print("Invalid input!")

                    elif choice == "a":
                        if user_account.role_id == 1:
                            name = input("Firstname of new admin: ")
                            lastname = input("Lastname of new admin: ")
                            username = f"qmina{count}"
                            email = f"qmin1{count}@company.nl"
                            password = hashlib.sha256("1234".encode())
                            password_hash = password.hexdigest()
                            mobile = input("What is the mobile number? ")

                            username = input("Username of new admin: ")
                            email = input("Email of new admin: ")
                            password = input("Password of new admin: ")
                            age = 0
                            db.create_admin_account(
                                con,
                                user_account.role_id,
                                2,
                                username,
                                email,
                                password_hash,
                                mobile,
                                name,
                                lastname,
                            )

                    elif choice == "d":
                        if choice:
                            print(db.get_all_users(con, user_account.role_id))
                            user_id = input("Which user do you want to delete? ")
                            if user_id:
                                db.delete_user(con, user_account.role_id, user_id)
                            else:
                                print("Invalid user. Please try again.")
                        else:
                            print("Invalid input. Please try again.")


                    elif choice == "c":
                        username = input("Username of new consultant: ")
                        email = input("Email of new consultant: ")
                        password = hashlib.sha256(input("New password: ").encode()).hexdigest()
                        name = input("Firstname of new consultant: ")
                        lastname = input("Lastname of new consultant: ")
                        mobile = input("What is the mobile number? ")

                        db.create_admin_account(
                                con,
                                user_account.role_id,
                                3,
                                username,
                                email,
                                password,
                                mobile,
                                name,
                                lastname,
                            )
                    elif choice == "n":
                        username = input("Username of new member: ")
                        email = input("Email of new member: ")
                        password = hashlib.sha256(input("New password: ").encode()).hexdigest()
                        name = input("Firstname of new member: ")
                        lastname = input("Lastname of new member: ")
                        mobile = input("What is the mobile number? ")
                        age = input("What is the age number? ")
                        gender = input("What is the gender number? ")
                        weight = input("What is the weight number? ")

                        db.create_admin_account(
                                con,
                                user_account.role_id,
                                4,
                                username,
                                email,
                                password,
                                mobile,
                                name,
                                lastname,
                                age,
                                gender,
                                weight

                            )
                    elif choice == "p":
                        user = db.authenticate_user(con,username,password)
                        current_password = hashlib.sha256(input("Your password: ").encode()).hexdigest()
                        if user.password == current_password:
                            new_password = hashlib.sha256(input("New password: ").encode()).hexdigest()
                            db.update_password(con,user.id,new_password)
                        else:
                            print("Incorrect password. Try Again")

                    elif choice == "4":
                        user = db.authenticate_user(con,username,password)
                        db.get_all_users(con,user.id)
                        account_id=input("UserID: ")
                        updated_user = db.get_user_by_id(con,int(account_id))
                        for key, value in updated_user:
                            if key not in ["id","fullname"]:
                                new_value = input(f"{key}: {value} ").strip()
                                if new_value:
                                    value=new_value
                                    setattr(updated_user,key,new_value)
                        db.update_user(con,user.id,updated_user.role_id, account_id, password,updated_user.username,updated_user.email,updated_user.mobile,
                                    updated_user.fullname.split(" ")[0],updated_user.fullname.split(" ")[1],
                                    updated_user.age,updated_user.gender,updated_user.weight)


if "__main__" == __name__:
    main()
