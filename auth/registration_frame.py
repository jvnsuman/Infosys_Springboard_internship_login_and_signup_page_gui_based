"""
FinSight - Register Frame
---------------------------
Tkinter ttk frame for new user registration.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

import database
from auth.security import (
    hash_password,
    is_valid_email,
    is_strong_password,
    generate_token,
    get_expiry,
)
from email_utils import send_verification_email
from config import VERIFICATION_TOKEN_EXPIRY_HOURS


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        title = ttk.Label(self, text="Create your FinSight account", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Name
        ttk.Label(self, text="Full Name").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.name_entry = ttk.Entry(self, width=35)
        self.name_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Email
        ttk.Label(self, text="Email").grid(row=3, column=0, sticky="w", pady=(5, 0))
        self.email_entry = ttk.Entry(self, width=35)
        self.email_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Password
        ttk.Label(self, text="Password").grid(row=5, column=0, sticky="w", pady=(5, 0))
        self.password_entry = ttk.Entry(self, width=35, show="*")
        self.password_entry.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Confirm Password
        ttk.Label(self, text="Confirm Password").grid(row=7, column=0, sticky="w", pady=(5, 0))
        self.confirm_entry = ttk.Entry(self, width=35, show="*")
        self.confirm_entry.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Label(
            self,
            text="Min 8 characters, with uppercase, lowercase,\nnumber, and special character.",
            foreground="#888",
            font=("Segoe UI", 8),
        ).grid(row=9, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Register button
        register_btn = ttk.Button(self, text="Register", command=self._handle_register)
        register_btn.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Link to login
        login_link = ttk.Label(self, text="Already have an account? Log in", foreground="#1565c0", cursor="hand2")
        login_link.grid(row=11, column=0, columnspan=2, pady=(5, 0))
        login_link.bind("<Button-1>", lambda e: self.controller.show_frame("LoginFrame"))

        self.columnconfigure(0, weight=1)

    def _clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)

    def _handle_register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        # ---- Validation ----
        if not name or not email or not password or not confirm:
            messagebox.showerror("Missing Fields", "Please fill in all fields.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if password != confirm:
            messagebox.showerror("Enter valid password", "Passwords do not match.")
            return

        valid, error_msg = is_strong_password(password)
        if not valid:
            messagebox.showerror("Weak Password", error_msg)
            return

        if database.email_exists(email):
            messagebox.showerror("Email Already Registered", "An account with this email already exists.")
            return

        # ---- Create user ----
        try:
            password_hash = hash_password(password)
            user_id = database.create_user(name, email, password_hash)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Could not create account:\n{e}")
            return

        # ---- Generate verification token and send email ----
        token = generate_token()
        expires_at = get_expiry(VERIFICATION_TOKEN_EXPIRY_HOURS)
        database.create_verification_token(user_id, token, expires_at)

        email_sent = send_verification_email(email, name, token)

        if email_sent:
            messagebox.showinfo(
                "Registration Successful",
                f"Account created!\n\nA verification link has been sent to {email}.\n"
                "Please check your inbox to verify your account.",
            )
        else:
            messagebox.showwarning(
                "Registration Successful (Email Failed)",
                "Account created, but we couldn't send the verification email.\n"
                "You can resend it later from the login screen.",
            )

        self._clear_fields()
        self.controller.show_frame("LoginFrame")
