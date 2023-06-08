from flask import session
from services.db import (db as default_db)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text

class Repository:
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
        session["role"] = role
        return True
    
#    def fixed_create_user(self, username, password, role):
#        hash_value = generate_password_hash(password)
#        values = {"username": username, "password": hash_value, "role": role}
#        sql = """INSERT INTO users (username, password, role)
#        VALUES (:username, :password, :role)"""
#        self._db.session.execute(text(sql), values)
#        self._db.session.commit()
#        session["username"] = username
#        session["role"] = role
#        return True
    
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
    
#    def fixed_sign_in(self, username, password):
#        values = {"username": username}
#        sql = """SELECT id, username, password, role FROM users WHERE username=:username"""
#        user = self._db.session.execute(text(sql), values).fetchone()
#        if not user:
#            return False
#        hash_password = user.password
#        if check_password_hash(hash_password, password):
#            return True
#        return False

    def _get_user_id(self):
        username = session["username"]
        sql = f"""SELECT id FROM users
        WHERE username='{username}'"""
        result = self._db.session.execute(text(sql)).fetchone()
        return result.id

    def get_user_role(self, username):
        sql = f"""SELECT role FROM users
        WHERE username='{username}'"""
        result = self._db.session.execute(text(sql)).fetchone()
        return result.role

    def create_post(self, post_text):
        # SQL injection
        user_id = self._get_user_id()
        sql = f"""INSERT INTO posts(user_id, text)
        VALUES ('{user_id}', '{post_text}')"""
        self._db.session.execute(text(sql))
        self._db.session.commit()
        return True
    
    def get_all_posts(self):
        sql = """SELECT posts.id, posts.text, posts.created_at, users.id AS user_id, users.username
                FROM posts
                LEFT JOIN users ON posts.user_id = users.id
                ORDER BY posts.created_at DESC
                LIMIT 100"""
        results = self._db.session.execute(text(sql)).fetchall()
        return results

    def delete_post(self, post_id):
        sql = f"""DELETE FROM posts
        WHERE id ='{post_id}'"""
        if self._db.session.execute(text(sql)):
            self._db.session.commit()
            return True
        return False
    
    def get_users(self):
        sql = """SELECT * FROM users"""
        results = self._db.session.execute(text(sql)).fetchall()
        return results

    def get_posts(self):
        sql = """SELECT * FROM posts"""
        results = self._db.session.execute(text(sql)).fetchall()
        return results


repository = Repository()