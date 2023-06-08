from flask import Flask
import secrets
from flask import render_template, request, jsonify, flash, redirect, session, abort
import json
from app import app
from services.repository import repository

@app.route("/")
def index():
    posts = repository.get_all_posts()
    return render_template("index.html", posts=posts)

@app.route("/users")
def users():
    file = open("data/users.json","r")
    data = json.loads(file.read())
    return jsonify(data)

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    if username or password == "" or None:
        flash("")
    if repository.search_user(username):
        flash("Username already exists!")
        return redirect("/")
    if repository.fixed_create_user(username, password, role=0):
        #session["csrf_token"] = secrets.token_hex(16)
        flash("User created successfully!")
        return redirect("/")

@app.route("/sign_out")
def sign_out():
    if session["username"]:
        del session["username"]
    if session["role"]:
        del session["role"]
    flash("Signed out")
    return redirect("/")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    username = request.form["username"]
    password = request.form["password"]
    if repository.fixed_sign_in(username, password):
        session["username"] = username
        role = repository.get_user_role(username)
        session["role"] = role
        #session["csrf_token"] = secrets.token_hex(16)
        flash(f"Signed in as {username}")
        return redirect("/")
    flash("Check username and password")
    return redirect("/")

@app.route("/post_text", methods=["POST"])
def post():
    post_text = request.form["post_text"]
    if len(post_text) < 1:
        # Error here to demo the debugger
        return error
    #if session["csrf_token"] != request.form["csrf_token"]:
        #abort(403)
    repository.create_post(post_text)
    flash("Posted on Bitter!")
    return redirect("/")

@app.route("/delete_post/<int:post_id>", methods=["POST", "GET"])
def delete_post(post_id):
    if session["role"] == 1:
        if repository.delete_post(post_id):
            flash("Post deleted")
            return redirect("/")
        flash("Something went wrong")
        return redirect("/")
    flash("Not authorised")
    return redirect("/")

@app.route("/api/users", methods=["GET"])
def get_users():
    if session["role"] == 1:
        data = repository.get_users()
        items = []
        for row in data:
            items.append({"id": row[0], 
                        "username": row[1],
                        "password": row[2],
                        "role": row[3]})
        return items
    flash("Not authorised")
    return redirect("/")

@app.route("/api/posts", methods=["GET"])
def get_posts():
    data = repository.get_posts()
    items = []
    for row in data:
        items.append({"id": row[0], 
                      "user_id": row[1],
                      "text": row[2],
                      "created_at": str(row[3])})
    return items

