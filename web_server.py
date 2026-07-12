"""
FinSight - Local Server Mini-Server
--------------------------------------
Runs in a background thread alongside the Tkinter app.
Only serves two purposes:
  1. /verify            - confirms a user's email when they click the verification link
  2. /reset-password    -shows a form and processes a new password when the user
                          clicks the password reset link from their email
"""

from flask import Flask, request, render_template
from datetime import datetime

import database
from auth.security import hash_password, is_strong_password, is_token_expired
from config import FLASK_CONFIG

app = Flask(__name__)

@app.route("/verify", methods=["GET"])
def verify_email():
    token = request.args.get("token", "")
    token_row =  database.get_verification_token(token)

    if not token_row:
        return render_template(
            "verify_success.html",
            success=False,
            title="Invalid Link",
            message="This verification link is invalid or does not exists."
        )
    
    if token_row["used"]:
        return render_template(
            "verify_success.html",
            success=False,
            title="Already Used",
            message="This verification link has already been used.",
        )
    
    if is_token_expired(token_row["expires_at"]):
        return render_template(
            "verify_success.html",
            success=False,
            title="Link Expired",
            message="this verification link has expires. Please request a new one from the app."
        )
    
    #All good - mark used as verified and token as used
    database.mark_user_verified(token_row["user_id"])
    database.mark_verification_token_used(token)

    return render_template(
        "verify_success.html",
        success=True,
        title="Email Verified!",
        message="Your email has been successfully verified. You can log in to finSight.",
    )


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("token", "")
    token_row = database.get_reset_token(token)

    #validate token existence
    if not token_row:
        return render_template(
            "verify_success.html",
            success=False,
            title="Invalid Link",
            message="This password reset link is invalid or does not exist."

        )
    
    if token_row["used"]:
        return render_template(
            "verify_success.html",
            success=False,
            title="Already Used",
            message="This password reset link has already been used.",
        )
    
    if is_token_expired(token_row["expires_at"]):
        return render_template(
            "verify_success.html",
            success=False,
            title="Link Expired",
            message="This password reset link has expired. Please request a new link to reset password."
        )
    if request.method == "GET":
        return render_template("reset_password.html", token=token, error=None)
    
    #POST - process the new password
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if new_password != confirm_password:
        return render_template(
            "reset_password.html", token=token, error="Password do not match."

        )
    valid, error_msg = is_strong_password(new_password)
    if not valid:
        return render_template("reset_password.html", token=token, error=error_msg)
    

    #Update password and invalidate token
    new_hash = hash_password(new_password)
    database.update_user_password(token_row["user_id"], new_hash)
    database.mark_reset_token(token)

    return render_template(
        "verify_success.html",
        success=True,
        title="Password Reset!",
        message="Your password has been successfully reset. You can now log in with your new password.",
    )

def run_flask_server():
    """Start the flask server. Intended to be run in the background thread."""
    app.run(
        host=FLASK_CONFIG["host"],
        port=FLASK_CONFIG["port"],
        debug=False,
        use_reloader=False,      # must be false when running in a  thread
    )