import sqlite3
from utils import load_private_key, load_public_key
import tkinter as tk

from app import App
from config import Config


if "__main__" == __name__:
    con = sqlite3.connect("data.db")
    config = Config(
        con=con,
        private_key=load_private_key(),
        public_key=load_public_key(),
    )

    # create the root window
    root = tk.Tk()
    app = App(root, config)
    app.run()

    # close the database connection
    con.close()
