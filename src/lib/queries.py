#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
test_users = ["user", "singlerider", "testuser"]

class Database:

    def __init__(self, name="twitch.db"):
        self.name = name
        self.con = lite.connect(self.name)

    def initiate(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT, points INT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS custom_commands(
                    id INTEGER PRIMARY KEY,
                    created_by TEXT, command TEXT,
                    response TEXT, times_used INT
                    , user_level TEXT);
                """)

    def add_user(self, users):
        user_tuples = [(x, x) for x in users]
        with self.con:
            cur = self.con.cursor()
            cur.executemany("""
                INSERT INTO users(id, username, points)
                    SELECT NULL, ?, 0
                    WHERE NOT EXISTS(
                        SELECT 1 FROM users WHERE username = ?);
                """, user_tuples)

    def remove_user(self, user="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM users WHERE username = '%s';
                """ % user)

    def get_user(self, user="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM users WHERE username = '%s'
                """ % user)
            user_data = cur.fetchone()
            return user_data

    def modify_points(self, user="testuser", points=5):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET points = '%d' WHERE username = '%s';
                """ % (points, user))

    def add_command(self, user="testuser", command="!test", response="{} check this out", user_level="mod"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO custom_commands(
                    id, created_by, command, response, times_used, user_level)
                    SELECT NULL, ?, ?, ?, 0, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM custom_commands WHERE command = ?);
                """, [user, command, response, user_level, command])

    def remove_command(self, command="!test"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM custom_commands WHERE command = '%s';
                """ % command)

    def modify_command(self, command="!test", response="different response"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET response = ?
                    WHERE command = ?
                """, [response, command])

    def increment_command(self, command="!test"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET times_used = times_used + 1
                    WHERE command = "%s"
                """ % command)

    def get_command(self, command="!test"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM custom_commands WHERE command = '%s'
                """ % command)
            command_data = cur.fetchone()
            return command_data

if __name__ == "__main__":
    db = Database("test.db")
    db.initiate()
    db.add_user(test_users)
    db.modify_points()
    print db.get_user()
    db.add_command()
    db.increment_command()
    db.increment_command()
    db.modify_command()
    db.increment_command()
    print db.get_command()
    db.get_command()
    raw_input("press enter to delete the test entries")
    db.remove_command()
    for user in test_users:
        db.remove_user(user)
