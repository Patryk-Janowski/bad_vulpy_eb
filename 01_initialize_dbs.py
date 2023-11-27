#!/usr/bin/env python3

import os
import sqlite3

def get_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"The file at {file_path} does not exist.")
    except PermissionError:
        print(f"You do not have permission to read the file at {file_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def db_init_users():
    home_path = os.environ.get("HOME")
    aws_credentials = get_file(f"{home_path}/.aws/credentials")

    users = [
        ('admin', 'SuperSecret'),
        ('elliot', '123123123'),
        ('tim', '12345678')
    ]

    conn = sqlite3.connect('db_users.sqlite')
    c = conn.cursor()
    home_path = os.environ.get("HOME")
    aws_credentials = get_file(f"{home_path}/.aws/credentials")
    c.execute("CREATE TABLE users (username text, password text, failures int, mfa_enabled int, mfa_secret text)")

    for u,p in users:
        c.execute("INSERT INTO users (username, password, failures, mfa_enabled, mfa_secret) VALUES ('%s', '%s', '%d', '%d', '%s')" %(u, p, 0, 0, ''))

    c.execute("CREATE TABLE conf (name text, keys text)")
    c.execute("INSERT INTO conf (name, keys) VALUES ('%s', '%s')" %("aws", aws_credentials))

    conn.commit()
    conn.close()


def db_init_posts():

    conn = sqlite3.connect('db_posts.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE posts (date date, username text, text text)")
    conn.commit()
    conn.close()


if __name__ == '__main__':

    try:
        os.remove('db_users.sqlite')
    except FileNotFoundError:
        pass
    try:
        os.remove('db_posts.sqlite')
    except FileNotFoundError:
        pass

    db_init_users()
    db_init_posts()

