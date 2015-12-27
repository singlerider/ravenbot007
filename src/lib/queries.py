#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
users = ["user", "singlerider", "testuser"]

class Database:

    def __init__(self, name="twitch"):
        self.name = name
        self.con = lite.connect(self.name)

    def initiate(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT, points INT, user_level TEXT);
                """)

    # can only be modified via twitch api
    def add_user(self, users):
        user_tuples = [(x, x) for x in users]
        with self.con:
            cur = self.con.cursor()
            cur.executemany("""
                INSERT INTO users(id, username, points, user_level)
                    SELECT NULL, ?, 0, 'reg'
                    WHERE NOT EXISTS(
                        SELECT 1 FROM users WHERE username = ?);
                """, user_tuples)

    def remove_user(self, user="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM users WHERE username = '%s';
                """ % user)

    def modify_points(self, user="testuser", points=5):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET points = '%d' WHERE username = '%s';
                """ % (points, user))

    def user_level(self, user="testuser", user_level="mod"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET user_level = '%s' WHERE username = '%s';
                """ % (user_level, user))

if __name__ == "__main__":
    db = Database("test.db")
    db.initiate()
    db.add_user(users)
    db.modify_points()
    db.user_level()
    raw_input("press enter to delete the test database")
    for user in users:
        db.remove_user(user)
