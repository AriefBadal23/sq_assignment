import database






def main():
    con = database.connect()
    # database.create_tables(con)


    

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
    """)
    # username = input("Username:")
    username = "super_admin"
    password = "Admin_123?"
    # password = input("Password:")
    while True:
        if username and password:
                user_account = database.get_user(con,username, password)
                if user_account != None:
                    if user_account.role_id == 1:
                        print(database.get_all_users(con))
                        choice = input(f""" 
            
                        Welcome, {user_account.username} choose one of the options below. Role: {user_account.role_id}: 
                        (q)uit, to Exit the program.
                        (s)how users and roles
                        (u)pdate user
                        (d)elete consultant
                        (r)eset consultant
                        (a)dd new admin
                        (u)pdate admin
                        (d)elete admin
                        (r)eset admin
                        (m)ake backup
                        (rb)restore backup
                        (l)ogs
                        (a)dd member
                        (u)pdate member
                        (d)elete member
                        (s)earch for member
                        """)
                        if choice == "q":
                            break
                        elif choice == "s":
                            pass
                        
                        elif choice == "u":
                            pass
                        
                        elif choice == "d":
                            pass
                    
                         
                         
                         
                         


    # database.register_consultant(con,"c3@company.nl","test12345","0612345677")
    # database.update_consultant(con,3,"0612345699")
    # database.delete_user(con,3)





if "__main__" == __name__:
    main()