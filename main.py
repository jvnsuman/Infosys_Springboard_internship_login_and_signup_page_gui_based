"""
FinSight - Main Application Entry Point
------------------------------------------
Launches:
  1. the local Flask mini-server (background thread)  for email verification and password reset links.
  2. The Tkinter desktop app
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

import database
from web_server import run_flask_server
from auth.login_frame import LoginFrame
from auth.registration_frame import RegisterFrame
from auth.forgot_password_frame import ForgotPasswordFrame
from auth.dashboard_frame import DashboardFrame


class FinSightApp(tk.Tk):
    """Main application window that manages frame-switching."""
    
    def __init__(self):
        super().__init__()

        self.title("FinSight - Personal Finance & Investment Intelligence")
        self.geometry("500x600")
        self.resizable(False, False)

        #holds the currently logged-in user's data (dict) or None
        self.current_user = None

        #container  that  stacked on the top of each other
        container  = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for FrameClass in (LoginFrame, RegisterFrame, ForgotPasswordFrame, DashboardFrame):
            frame_name = FrameClass.__name__
            frame = FrameClass(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self,frame_name: str):
        """Raise the requested frame to the top of the stack."""
        frame = self.frames[frame_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

def start_flask_background():
    """Run the Flask server in a daemon thread so it shuts down with the app."""
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()

def main():
    #Initialise database and tables
    try:
        database.init_db()
    except Exception as e:
        # show a plane error dialog if the mysql isn't reachable, then exit
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Database Connection Failed",
            f"Could not connect to MySQL.\n\n"
            f"Please check your config.py setting and ensure MySQL is running. \n\nError: {e}",

        )
        root.destroy()
        return
    
    #start the local flask server in the background
    start_flask_background()

    #launch the tkinter app
    app = FinSightApp()
    app.mainloop()


if __name__ == "__main__":
    main()

