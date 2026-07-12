"""
FinSight - Login Frame
-------------------------
Tkinter ttk frame for user login.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import database
from auth.security import verify_password, is_valid_email, generate_token, get_expiry
from email_utils import send_verification_email
from config import VERIFICATION_TOKEN_EXPIRY_HOURS


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        title = ttk.Label(self, text="Log in to FinSight", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Email
        ttk.Label(self, text="Email").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.email_entry = ttk.Entry(self, width=35)
        self.email_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Password
        ttk.Label(self, text="Password").grid(row=3, column=0, sticky="w", pady=(5, 0))
        self.password_entry = ttk.Entry(self, width=35, show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        # Forgot password link
        forgot_link = ttk.Label(self, text="Forgot password?", foreground="#1565c0", cursor="hand2", font=("Segoe UI", 9))
        forgot_link.grid(row=5, column=0, columnspan=2, sticky="e", pady=(0, 15))
        forgot_link.bind("<Button-1>", lambda e: self.controller.show_frame("ForgotPasswordFrame"))

        # Login button
        login_btn = ttk.Button(self, text="Log In", command=self._handle_login)
        login_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Link to register
        register_link = ttk.Label(self, text="Don't have an account? Register", foreground="#1565c0", cursor="hand2")
        register_link.grid(row=7, column=0, columnspan=2, pady=(5, 0))
        register_link.bind("<Button-1>", lambda e: self.controller.show_frame("RegisterFrame"))

        self.columnconfigure(0, weight=1)

    def _clear_fields(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def _handle_login(self):
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Missing Fields", "Please enter both email and password.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        user = database.get_user_by_email(email)

        if not user or not verify_password(password, user["password_hash"]):
            messagebox.showerror("Login Failed", "Incorrect email or password.")
            return

        # Successful login
        self.controller.current_user = user
        self._clear_fields()

        if not user["is_verified"]:
            self._show_unverified_reminder(user)

        self.controller.show_frame("DashboardFrame")

    def _show_unverified_reminder(self, user):
        answer = messagebox.askyesno(
            "Email Not Verified",
            "Your email is not verified yet.\n\n"
            "Some features may be limited until you verify.\n"
            "Would you like us to resend the verification email?",
        )
        if answer:
            token = generate_token()
            expires_at = get_expiry(VERIFICATION_TOKEN_EXPIRY_HOURS)
            database.create_verification_token(user["id"], token, expires_at)
            sent = send_verification_email(user["email"], user["name"], token)
            if sent:
                messagebox.showinfo("Email Sent", f"A new verification link was sent to {user['email']}.")
            else:
                messagebox.showwarning("Email Failed", "Could not send verification email. Please try again later.")



