# CSB Project 1

This repository contains the [Cyber Security Base Project 1](https://cybersecuritybase.mooc.fi/module-3.1) project.

## Disclaimer

The code in this repository is for demo purposes only and not to be run in public internet or distributed.

## Bitter

Bitter - a bit like twitter. With a severely faulty security configuration.

#### Features

- Creating a user

- Posting on public feed

- Sign in and Sign out

## Installation

- Make sure you have Python 3.10 or newer installed.

- Install PostgreSQL on your computer with [these](https://github.com/hy-tsoha/local-pg) instructions.

- Run PostgreSQL locally and keep it running while using the app.

- Clone this repository on your computer.

- Create a file called ```.env``` in the root of the application

- Write ```DATABASE_URL=postgresql:///_your_username_``` in the .env file

- Write ```SECRET_KEY=_random_combination_of_digits_and_numbers_``` in the file

- Tip! you can create a random string as follows:

``` python3 ```

``` import secrets ```

``` secrets.token_hex(16) ```

- Run ``` pip install -r requirements.txt ``` to install dependencies.

- Run ``` psql < schema.sql ``` to create tables to the database.

- Run ``` bash start.sh ``` in the root of the application to launch the app.

- Navigate to ```http://localhost:5000/``` to use it.

## Vulnerabilities

### 1. A03:2021 – Injection

https://github.com/evahteri/csb-project-1/blob/d4c55eed3546b3e54c961dce9f4b85e4bd620e93/services/repository.py#L9

and 

https://github.com/evahteri/csb-project-1/blob/d4c55eed3546b3e54c961dce9f4b85e4bd620e93/services/repository.py#L51

Injection is a flaw in the program where user inputted data is not validated or sanitized, but rather accepted inside the database raw. In this case the injection is an SQL injection which allows the user to alter the SQL command used to save data into the database

#### Fix

User input should not be inserted straight into the SQL string, but through using separate entity to store values.

Here is the fixed user creation function:

https://github.com/evahteri/csb-project-1/blob/eebcd7504536355c82247a824c3b3f5489c3520b/services/repository.py#L21

    def fixed_create_user(self, username, password, role):
        hash_value = generate_password_hash(password)
        values = {"username": username, "password": hash_value, "role": role}
        sql = """INSERT INTO users (username, password, role)
        VALUES (:username, :password, :role)"""
        self._db.session.execute(text(sql), values)
        self._db.session.commit()
        session["username"] = username
        session["role"] = role
        return True

The create_post function ought to be fixed in the same way.

### 2. A01:2021 – Broken Access Control

https://github.com/evahteri/csb-project-1/blob/eebcd7504536355c82247a824c3b3f5489c3520b/schema.sql#L15

and

https://github.com/evahteri/csb-project-1/blob/eebcd7504536355c82247a824c3b3f5489c3520b/routes.py#L74

Broken access control allows users to get access to functions or data that is not within their user's limits. In this application there is a major flaw that fall into this category: In schema.sql, an admin user is created with a poor combination of username and password (username: admin, password: admin). Access to this user allows anyone to delete posts from the website and to get all user data from an API via http://localhost:5000/api/users. It includes sensitive data such as passwords.

#### Fix 

Do not create an admin user with poor password. Every admin user should be created with unique username and password. Remove the line from schema.sql and use psql to create your own admin user.

Do not use the application's backend to serve as an open backend. Remove the APIs from routes.py.

### 3.A02:2021 – Cryptographic Failures

https://github.com/evahteri/csb-project-1/blob/66c48e35a243843fc52c957f8b0b001c98c9be02/services/repository.py#L10

Cryptographic failures are flaws in the application that compromise password and login security. Storing sensitive data needs extra protection and failing to do so, might allow sensitive data to fall into attacker's hands. In context of this application, the sensitive data in case is passwords. They should be crypted when inserted to the database, but they are not.

#### Fix

Create a hash password when saving. Here is the fixed function:

https://github.com/evahteri/csb-project-1/blob/eebcd7504536355c82247a824c3b3f5489c3520b/services/repository.py#L2

    def fixed_create_user(self, username, password, role):
        hash_value = generate_password_hash(password)
        values = {"username": username, "password": hash_value, "role": role}
        sql = """INSERT INTO users (username, password, role)
        VALUES (:username, :password, :role)"""
        self._db.session.execute(text(sql), values)
        self._db.session.commit()
        session["username"] = username
        session["role"] = role
        return True

Remember to alter the sign in function to match:

https://github.com/evahteri/csb-project-1/blob/5647ad0148ab418ce208796e25462dac81efb88e/services/repository.py#L50

    def fixed_sign_in(self, username, password):
        values = {"username": username}
        sql = """SELECT id, username, password, role FROM users WHERE username=:username"""
        user = self._db.session.execute(text(sql), values).fetchone()
        if not user:
            return False
        hash_password = user.password
        if check_password_hash(hash_password, password):
            return True
        return False

### 4.Missing CSRF protection

https://github.com/evahteri/csb-project-1/blob/ab3f3e3e7f09cd3507bfbfc406349a4091e80ecb/templates/index.html#L41

Missing CSRF protection allows users that are not signed in to use forms to insert data. The application does not check that a page request is made by a logged in user. If a signed in user is lured into an external page that calls the application's function to create a new post, the post would be created and the post would seem that it is sent by the user that is signed in.

#### Fix

There should be a secret CSRF token to check if the form is sent from the right source.

This can be done by adding these lines:

- https://github.com/evahteri/csb-project-1/blob/ae63ab0e4c08f5ecbbd3b215cb40eb436a1a1fcf/routes.py#L62

- https://github.com/evahteri/csb-project-1/blob/ae63ab0e4c08f5ecbbd3b215cb40eb436a1a1fcf/routes.py#L29

- https://github.com/evahteri/csb-project-1/blob/ae63ab0e4c08f5ecbbd3b215cb40eb436a1a1fcf/routes.py#L62

- https://github.com/evahteri/csb-project-1/blob/ae63ab0e4c08f5ecbbd3b215cb40eb436a1a1fcf/templates/index.html#L45


What these changes do: creates a unique CSRF key for the session and then the key is checked to validate user.

### 5. A05:2021 – Security Misconfiguration

https://github.com/evahteri/csb-project-1/blob/218980832eb16fa3b393215bf399b3a5d5fdb110/start.sh#L3

Security misconfiguration happens when an application is configured so that it leaves vulnerabilities open. This can be unnecessary opened ports, improperly configured security settings, improper error handling etc. In this application, the application is run in debug mode which results in overly informative error messages.

When trying to post an empty post with the application, an error occurs, showing detailed information about the error. The attacker can now open details about the function that caused the error and see that the CSRF protection is commented out, thus revealing a vulnerability in the application.

#### Fix

Do not run the flask application in debug mode. Remove the tag ```--debug``` from the start script.