# FinSight — Personal Finance & Investment Intelligence (Login & Signup) 🔐💰

> ⚠️ **All Rights Reserved**
> This repository is for portfolio and showcase purposes only.
> Do not copy, reuse, or redistribute without explicit permission from the author.

---

## 📌 About

**FinSight** is a Python desktop application (Tkinter-based) for personal finance and investment intelligence, developed as part of the **Infosys Springboard Virtual Internship 7.0**.

This repository contains the **authentication module** of FinSight — a secure login and signup system with email verification and password reset, built using **Tkinter**, **Flask**, **MySQL**, and **bcrypt**.

---

## 💡 How It Works

FinSight runs as a hybrid desktop + local web app:

1. **Tkinter Desktop App** — the main GUI with Login, Registration, Forgot Password, and Dashboard screens
2. **Flask Mini-Server** — runs in a background thread alongside the Tkinter app, handling:
   - `/verify` — confirms a user's email when they click the verification link sent to their inbox
   - `/reset-password` — shows a secure form and processes password resets via emailed links
3. **MySQL Database** — stores user accounts, verification tokens, and password reset tokens

On startup, the app initializes the database connection, launches the Flask server in a daemon thread, then opens the Tkinter GUI starting on the Login screen.

---

## 🔐 Security Features

- **Bcrypt password hashing** — passwords are never stored in plaintext
- **Secure token generation** — URL-safe tokens (`secrets.token_urlsafe`) for email verification and password reset links, with configurable expiry windows
- **Password strength validation** — enforces minimum length, uppercase, lowercase, digit, and special character requirements
- **Email format validation** — regex-based email checks
- **Token expiry & single-use enforcement** — verification/reset links expire and can't be reused once redeemed

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Tkinter | Desktop GUI framework |
| Flask | Local mini-server for email verification & password reset links |
| MySQL (`mysql-connector-python`) | Database for users & tokens |
| bcrypt | Secure password hashing |
| Jinja2 / HTML templates | Rendered pages for verification & reset flows |

---

## 📂 Project Structure

```
Infosys_Springboard_internship_login_and_signup_page_gui_based/
│
├── main.py                          # App entry point — launches Flask thread + Tkinter GUI
├── database.py                      # MySQL connection & queries (users, tokens)
├── email_utils.py                   # Sends verification & password reset emails
├── web_server.py                    # Flask routes: /verify, /reset-password
├── config.py                        # DB & Flask config (excluded via .gitignore — contains secrets)
│
├── auth/
│   ├── login_frame.py               # Login screen (Tkinter frame)
│   ├── registration_frame.py        # Signup screen (Tkinter frame)
│   ├── forgot_password_frame.py     # Forgot password screen (Tkinter frame)
│   ├── dashboard_frame.py           # Post-login dashboard (Tkinter frame)
│   └── security.py                  # Password hashing, token generation, validation
│
└── templates/
    ├── verify_success.html          # Shown after email verification attempt
    └── reset_password.html          # Password reset form
```

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/jvnsuman/Infosys_Springboard_internship_login_and_signup_page_gui_based.git
   cd Infosys_Springboard_internship_login_and_signup_page_gui_based
   ```

2. Install dependencies:
   ```bash
   pip install flask mysql-connector-python bcrypt
   ```

3. Create your own `config.py` (not included in this repo) with your MySQL credentials and Flask host/port settings, e.g.:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "your_mysql_user",
       "password": "your_mysql_password",
       "database": "finsight_db"
   }

   FLASK_CONFIG = {
       "host": "127.0.0.1",
       "port": 5000
   }
   ```

4. Make sure MySQL is running, then launch the app:
   ```bash
   python main.py
   ```

---

## 🏫 Internship

This project was developed as part of the **Infosys Springboard Virtual Internship 7.0** — a self-paced virtual internship program by Infosys.

---

## 👤 Author

**Jivan Suman**
GitHub: [@jvnsuman](https://github.com/jvnsuman)

---

© 2026 Jivan Suman. All Rights Reserved.
