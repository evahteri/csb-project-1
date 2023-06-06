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
