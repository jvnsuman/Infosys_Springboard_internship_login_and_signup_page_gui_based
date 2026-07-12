"""
FInSight - Dashboard Frame (Placeholder)
-------------------------------------------
Shown after successful login. 
just a temporary dashboard.
"""

from tkinter import ttk

class DashboardFrame (ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        self.welcome_label = ttk.Label(self, text="", font=("Segoe UI", 18, "bold"))
        self.welcome_label.pack(anchor="w", pady=(0, 20))

        self.status_label = ttk.Label(self, text="", foreground="#c62828", font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", pady=(0,  20))

        ttk.Label(
            self,
            text="This is your FinSight dashboard. \n Expense tracking, budgets, and investment \n modules will appear in future update.",
            foreground="#666",
        ).pack(anchor="w",  pady=(0, 20))

        logout_btn = ttk.Button(self, text="Log Out", command=self._handle_logout)
        logout_btn.pack(anchor="w")

    def on_show(self):
        """Called every time this is shown, to refresh the greeting."""
        user = self.controller.current_user
        if user:
            self.welcome_label.config(text=f"Welcome, {user['name']}!")
            if not user["is_verified"]:
                self.status_label.config(text="⚠ Your email is not verified yet.")
            else:
                self.status_label.config(text="")

    def _handle_logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")
