import sqlite3
import tkinter as tk
from tkinter import messagebox


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Login")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        # Initialize local database
        self.init_db()

        # Render Main Login Frame
        self.create_login_screen()

    def init_db(self):
        """Creates the SQLite database and users table if they do not exist."""
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL
            )
        """
        )
        conn.commit()
        conn.close()

    def create_login_screen(self):
        """Builds the login UI layout."""
        self.clear_screen()

        # Title Frame
        title_label = tk.Label(
            self.root,
            text="Student Portal Login",
            font=("Arial", 18, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        title_label.pack(pady=(40, 20))

        # Form Container
        form_frame = tk.Frame(self.root, bg="#f4f6f9")
        form_frame.pack(pady=10)

        # Username Field
        tk.Label(
            form_frame,
            text="Username:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f9",
            fg="#34495e",
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.username_entry.grid(row=1, column=0, pady=(0, 15))

        # Password Field
        tk.Label(
            form_frame,
            text="Password:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f9",
            fg="#34495e",
        ).grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(
            form_frame, font=("Arial", 11), width=25, show="*"
        )
        self.password_entry.grid(row=3, column=0, pady=(0, 20))

        # Login Button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=("Arial", 10, "bold"),
            bg="#2980b9",
            fg="white",
            width=23,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.authenticate_user,
        )
        login_btn.grid(row=4, column=0, pady=10)

        # Register Switch Button
        reg_btn = tk.Button(
            form_frame,
            text="Create New Account",
            font=("Arial", 9, "underline"),
            bg="#f4f6f9",
            fg="#7f8c8d",
            bd=0,
            cursor="hand2",
            command=self.create_register_screen,
        )
        reg_btn.grid(row=5, column=0, pady=5)

    def create_register_screen(self):
        """Builds the registration UI layout."""
        self.clear_screen()

        title_label = tk.Label(
            self.root,
            text="Register Student Account",
            font=("Arial", 16, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        title_label.pack(pady=(30, 20))

        form_frame = tk.Frame(self.root, bg="#f4f6f9")
        form_frame.pack(pady=10)

        # Full Name
        tk.Label(
            form_frame, text="Full Name:", font=("Arial", 10, "bold"), bg="#f4f6f9"
        ).grid(row=0, column=0, sticky="w", pady=2)
        self.reg_fullname_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.reg_fullname_entry.grid(row=1, column=0, pady=(0, 10))

        # Username
        tk.Label(
            form_frame, text="Username:", font=("Arial", 10, "bold"), bg="#f4f6f9"
        ).grid(row=2, column=0, sticky="w", pady=2)
        self.reg_username_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.reg_username_entry.grid(row=3, column=0, pady=(0, 10))

        # Password
        tk.Label(
            form_frame, text="Password:", font=("Arial", 10, "bold"), bg="#f4f6f9"
        ).grid(row=4, column=0, sticky="w", pady=2)
        self.reg_password_entry = tk.Entry(
            form_frame, font=("Arial", 11), width=25, show="*"
        )
        self.reg_password_entry.grid(row=5, column=0, pady=(0, 15))

        # Register Submit Button
        submit_btn = tk.Button(
            form_frame,
            text="Register",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            width=23,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.register_user,
        )
        submit_btn.grid(row=6, column=0, pady=10)

        # Back to Login Button
        back_btn = tk.Button(
            form_frame,
            text="Back to Login",
            font=("Arial", 9, "underline"),
            bg="#f4f6f9",
            fg="#7f8c8d",
            bd=0,
            cursor="hand2",
            command=self.create_login_screen,
        )
        back_btn.grid(row=7, column=0)

    def authenticate_user(self):
        """Validates credentials against database records."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Input Error", "Please fill in all fields."
            )
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT full_name FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", f"Welcome, {user[0]}!")
            self.open_dashboard(user[0])
        else:
            messagebox.showerror(
                "Authentication Failed", "Invalid Username or Password."
            )

    def register_user(self):
        """Saves a new user record into the database."""
        fullname = self.reg_fullname_entry.get().strip()
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()

        if not fullname or not username or not password:
            messagebox.showwarning(
                "Input Error", "All fields are required."
            )
            return

        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
                (username, password, fullname),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Success", "Registration successful! Please login."
            )
            self.create_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error", "Username already exists. Choose another."
            )

    def open_dashboard(self, student_name):
        """Placeholder screen shown upon successful authentication."""
        self.clear_screen()
        self.root.geometry("500x300")

        tk.Label(
            self.root,
            text=f"Welcome, {student_name}!",
            font=("Arial", 16, "bold"),
            bg="#f4f6f9",
            fg