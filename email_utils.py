"""
FinSight - Email Utility
------------------------
sends verification and password reset email via Gmail SMTP.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart

from config import  EMAIL_CONFIG, FLASK_CONFIG

def _send_email(to_email: str, subject: str, html_body: str) -> bool:
    """Internal helper to send an HTML email via Gmail SMTP. Returns True on success."""
    try:
        msg = MIMEMultipart("alternative")
        msg["subject"] = subject
        msg["from"] = EMAIL_CONFIG["sender_email"]
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["app_password"])
            server.sendmail(EMAIL_CONFIG["sender_email"], to_email, msg.as_string())

        return True
    except Exception as e:
        print(f"[Email Error] Failed to send email to {to_email}: {e}")
        return False
    

def send_verification_email(to_email: str, name: str, token: str) -> bool:
    """Send an account verification email with a link to the local Flask server."""
    base_url = f"http://{FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}"
    verify_link = f"{base_url}/verify?token={token}"

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Welcome to FinSight, {name}!</h2>
        <p>Thanks for registering. Please verify your email address by clicking the link below:</p>
        <p>
          <a href="{verify_link}"
             style="background-color:#2e7d32;color:white;padding:10px 20px;
                    text-decoration:none;border-radius:5px;display:inline-block;">
            Verify My Email
          </a>
        </p>
        <p>Or copy and paste this link into your browser:</p>
        <p>{verify_link}</p>
        <p>This link will expire in 24 hours.</p>
      </body>
    </html>
    """
    return _send_email(to_email, "Verify your FinSight account", html_body)


def send_password_reset_email(to_email: str, name: str, token: str) -> bool:
    """send a password reset email with the link to the local flask reset form."""
    base_url = f"http://{FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}"
    reset_link = f"{base_url}/reset-password?token={token}"

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Password Reset Request</h2>
        <p>Hello {name},</p>
        <p>We received a request to reset your FinSight account password. Click the button below to set a new password:</p>
        <p>
          <a href="{reset_link}"
             style="background-color:#d32f2f;color:white;padding:10px 20px;
                    text-decoration:none;border-radius:5px;display:inline-block;">
            Reset My Password
          </a>
        </p>
        <p>Or copy and paste this link into your browser:</p>
        <p>{reset_link}</p>
        <p>This link will expire in 1 hour.</p>
      </body>
    </html>
    """
    return _send_email(to_email, "Reset your FinSight password", html_body)

