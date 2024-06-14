import tkinter as tk
from tkinter import messagebox


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Username Label and Entry
        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Input Error", "Please enter both username and password"
            )
            return

        # Dummy check for the purpose of this example
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login Success", "Welcome Admin!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
