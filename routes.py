from flask import Flask
from flask import render_template, request, jsonify, flash, redirect, session
import json
from app import app
from services.repository import user_repository

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def users():
    file = open("data/users.json","r")
    data = json.loads(file.read())
    return jsonify(data)

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    if user_repository.search_user(username):
        flash("Username already exists!")
        return redirect("/")
    if user_repository.create_user(username, password, role=0):
        flash("User created successfully!")
        return redirect("/")

@app.route("/sign_out")
def sign_out():
    if session["username"]:
        del session["username"]
    flash("Signed out")
    return redirect("/")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    username = request.form["username"]
    password = request.form["password"]
    if user_repository.sign_in(username, password):
        session["username"] = username
        flash(f"Signed in as {username}")
        return redirect("/")
    flash("Check username and password")
    False

