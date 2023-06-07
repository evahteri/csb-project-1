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

## How to run

- Make sure you have Python 3.10 or newer installed.

- Install PostgreSQL on your computer with [these](https://github.com/hy-tsoha/local-pg) instructions.

- Run PostgreSQL locally and keep it running while using the app.

- Clone this repository on your computer.

- Create a file called .env in the root of the application

- Write DATABASE_URL=postgresql:///_your_username_ in the file

- Write SECRET_KEY=_random_combination_of_digits_and_numbers_ in the file

- Tip! you can create a random secret as follows:

``` python3 ```

``` import secrets ```

``` secrets.token_hex(16) ```

And then copy the string to the .env file.

- Run ``` pip install -r requirements.txt ``` to install dependencies.

- Run ``` psql < schema.sql ``` to create tables to the database.

- Run ``` bash start.sh ``` in the root of the application.

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

