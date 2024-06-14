# import hashlib
# from database import initialize_database_tables, connect
# import db
import tkinter as tk
from app import App
from db_init import initialize_database_tables, connect


if "__main__" == __name__:
    # set up the database
    initialize_database_tables()
    con = connect()

    # create the root window
    root = tk.Tk()
    app = App(root, con)
    app.run()
    root.mainloop()

    con.close()
