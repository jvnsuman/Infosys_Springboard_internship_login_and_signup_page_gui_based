"""
FinSight - Forgot Password Frame
----------------------------------
Tkinter ttk frame where the user enters their email to receive 
a password reset link (handled by the local Flask server).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database
from auth.security import is_valid_email, generate_token, get_expiry
from email_utils import send_password_reset_email
from config import RESET_TOKEN_EXPIRY_HOURS


class ForgotPasswordFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        title = ttk.Label(self, text="Reset Your Password", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        subtitle = ttk.Label(
            self,
            text="Enter your account email and we'll send you\na link to reset your  password.",
            foreground="#666"
        )
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

        ttk.Label(self, text="Email").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.email_entry = ttk.Entry(self, width=35)
        self.email_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        send_btn = ttk.Button(self, text="Send Reset Link", command=self._handle_send_reset)
        send_btn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        back_link = ttk.Label(self, text="Back to Login", foreground="#1565c0", cursor="hand2")
        back_link.grid(row=5, column=0, columnspan=2, pady=(5, 0))
        back_link.bind("<Button-1>", lambda e: self.controller.show_frame("LoginFrame"))

        self.columnconfigure(0, weight=1)

    def _clear_fields(self):
        self.email_entry.delete(0, tk.END)

    def _handle_send_reset(self):
        email = self.email_entry.get().strip().lower()

        if not email:
            messagebox.showerror("Missing Email", "Please enter your email address.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        user = database.get_user_by_email(email)

        # Do not reveal whether the email exists or not (security best practice)
        if user:
            token = generate_token()
            expires_at = get_expiry(RESET_TOKEN_EXPIRY_HOURS)
            database.create_reset_token(user["id"], token, expires_at)
            send_password_reset_email(user["email"], user["name"], token)

        messagebox.showinfo(
            "Check Your Email",
            f"If an account exists for {email}, a password reset link has been sent.\n"
            "The link will expire in 1 hour.",
        )

        self._clear_fields()
        self.controller.show_frame("LoginFrame")
