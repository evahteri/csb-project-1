from flask import session
from services.db import (db as default_db)
from sqlalchemy.sql import text

class UserRepository:
    def __init__(self, db=default_db):
        self._db = db

    def create_user(self, username, password, role):
        # SQL injection
        # Unsafe method of saving passwords
        sql = f"""INSERT INTO users (username, password, role)
        VALUES ('{username}', '{password}', {role})"""
        self._db.session.execute(text(sql))
        self._db.session.commit()
        session["username"] = username
        return True
    
    def search_user(self, username):
        sql = f"""SELECT username
        FROM users
        WHERE username='{username}'
        """
        return bool(self._db.session.execute(text(sql)).fetchall())

    def sign_in(self, username, password):

        sql = f"""SELECT id, username, password, role 
        FROM users WHERE username='{username}'"""
        user = self._db.session.execute(text(sql)).fetchone()
        if not user:
            return False
        if not user.password == password:
            return False
        return True

user_repository = UserRepository()