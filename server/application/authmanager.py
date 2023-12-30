import datetime
import sqlite3

import jwt as jwt


class AuthManager:
    DB_NAME: str = 'auth.db'
    SECRET_KEY: str = 'zort'
    BLACKLISTED_TOKENS: set[str] = set()

    @staticmethod
    def initialize():
        conn = sqlite3.connect(AuthManager.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def register(username, password) -> (bool, str):
        conn = sqlite3.connect(AuthManager.DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return True, "Registration successful."
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Username already exists."

    @staticmethod
    def login(username, password) -> (bool, str, str | None):
        conn = sqlite3.connect(AuthManager.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            token = AuthManager.generate_token(username)
            return True, "Login successful.", token
        else:
            return False, "Invalid username or password.", None

    @staticmethod
    def logout(token) -> str:
        if AuthManager.is_authenticated(token):
            AuthManager.invalidate_token(token)
            return "Logged out."
        else:
            return "Already logged out."

    @staticmethod
    def is_authenticated(token) -> bool:
        return AuthManager.get_username_from_token(token) is not None

    @staticmethod
    def generate_token(username) -> str:
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, AuthManager.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def get_username_from_token(token) -> str | None:
        if token in AuthManager.BLACKLISTED_TOKENS:
            return None

        try:
            payload = jwt.decode(token, AuthManager.SECRET_KEY, algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def invalidate_token(token):
        AuthManager.BLACKLISTED_TOKENS.add(token)
