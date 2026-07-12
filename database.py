"""
FinSight - Database Layer
--------------------------
Handles MySQL connection, schema creation, and all queries
related tp users, email verification tokens, and password reset tokens.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_connection():
    """Create and return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"],
        )
        return conn
    except Error as e:
        print(f"[Database Error] Could not connect to MySQL: {e}")
        raise

def init_db():
    """
    Create the database (if it doesn't exist) and all required tables.
    Should be run once at application startup.
    """
    # connect without specifying a database, to create it if needed
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
    conn.commit()
    cursor.close()
    conn.close()

    # connect to the actual database and create tables
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(100) NOT NULL,
                   email VARCHAR(150) NOT NULL UNIQUE,
                   password_hash VARCHAR(255) NOT NULL,
                   role VARCHAR(20) NOT NULL DEFAULT 'User',
                   is_verified BOOLEAN NOT NULL DEFAULT FALSE,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
               """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS verification_tokens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token VARCHAR(255) NOT NULL UNIQUE,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_reset_tokens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token VARCHAR(255) NOT NULL UNIQUE,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
    

    conn.commit()
    cursor.close()
    conn.close()
    print("[Database] Tables verified/created successfully.")


# ------------ User Queries ------------
def create_user(name, email, password_hash):
    """Insert a new user. Returns the new users id."""
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
        (name, email, password_hash),
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def get_user_by_email(email):
    """Fetch a userby email. Returns a dictionary or none ."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users where email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Fetch a user by id. Return a dictionary or none."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def email_exists(email):
    """Check if an email is already registered."""
    return get_user_by_email(email) is not None

def mark_user_verified(user_id):
    """Mark a user as Verified."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_verified = TRUE WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_user_password(user_id, new_password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password_hash = %s WHERE id = %s",
        (new_password_hash, user_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

# -----------  Verification Token Queries -----------

def create_verification_token(user_id, token, expires_at):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO verification_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
        (user_id, token, expires_at),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_verification_token(token):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM verification_tokens WHERE token = %s", (token,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def mark_verification_token_used(token):
    conn  = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE verification_tokens SET used = TRUE WHERE token = %s", (token,)
    )
    conn.commit()
    cursor.close()
    conn.close()


# ----------------- Password Reset Token Queries -----------------
def create_reset_token(user_id, token, expires_at):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
        (user_id, token, expires_at),
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_reset_token(token):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM password_reset_tokens WHERE token = %s", (token,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def mark_reset_token(token):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE password_reset_tokens SET used = TRUE WHERE token = %s", (token,)
    )
    conn.commit()
    cursor.close()
    conn.close()

