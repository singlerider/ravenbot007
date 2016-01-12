#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
test_users = ["user", "singlerider", "testuser"]


class Database:

    def __init__(self, name="twitch.db"):
        self.name = name
        self.con = lite.connect(self.name, check_same_thread=False)

    def initiate(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT, points INT, channel TEXT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS custom_commands(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    created_by TEXT, command TEXT,
                    response TEXT, times_used INT
                    , user_level TEXT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quotes(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    created_by TEXT, quote TEXT,
                    quote_number INT, game TEXT);
                """)

    def add_user(self, users, channel):
        user_tuples = [(x, channel, x, channel) for x in users]
        with self.con:
            cur = self.con.cursor()
            cur.executemany("""
                INSERT INTO users(id, username, points, channel)
                    SELECT NULL, ?, 0, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM users WHERE username = ?
                        AND channel = ?);
                """, user_tuples)

    def remove_user(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM users WHERE username = ? and channel = ?;
                """, [user, channel])

    def get_user(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM users WHERE username = ? and channel = ?
                """, [user, channel])
            user_data = cur.fetchone()
            return user_data

    def modify_points(self, user="testuser", channel="testchannel", points=5):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET points = points + ? WHERE username = ?
                    AND channel = ?;
                """, [points, user, channel])

    def add_command(
            self, user="testuser", command="!test",
            response="{} check this out", user_level="reg",
            channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO custom_commands(
                    id, channel, created_by, command, response,
                    times_used, user_level)
                    SELECT NULL, ?, ?, ?, ?, 0, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM custom_commands
                            WHERE command = ? and channel = ?);
                """, [channel, user, command, response,
                        user_level, command, channel])

    def remove_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM custom_commands
                    WHERE command = ? AND channel = ?;
                """, [command, channel])

    def modify_command(
            self, command="!test", response="different response",
            channel="testuser", user_level="mod"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET response = ?, user_level = ?
                    WHERE command = ? AND channel = ?;
                """, [response, user_level, command, channel])

    def increment_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET times_used = times_used + 1
                    WHERE command = ? AND channel = ?;
                """, [command, channel])

    def get_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM custom_commands
                    WHERE command = ? AND channel = ?;
                """, [command, channel])
            command_data = cur.fetchone()
            return command_data

    def add_quote(
            self, channel="testchannel", user="testuser",
            quote="quote", game="testgame"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT count(0) FROM quotes WHERE channel = '%s'
                """ % channel)
            count = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO quotes VALUES (NULL, ?, ?, ?, ?, ?)
                """, [channel, user, quote, count + 1, game])

    def remove_quotes(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM quotes WHERE channel = '%s'
                """ % channel)

    def get_quote(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM quotes WHERE channel = '%s'
                    ORDER BY RANDOM() LIMIT 1;
                """ % channel)
            quote = cur.fetchone()
            return quote

    def get_cash_rank(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT a1.username, a1.points, a1.channel,
                    COUNT (a2.points) points_rank
                    FROM users a1, users a2
                    WHERE a1.points < a2.points
                    OR (a1.points=a2.points
                    AND a1.username = a2.username)
                    GROUP BY a1.username, a1.points
                    HAVING a1.username = ?
                    AND a1.channel = ?
                    ORDER BY a1.points DESC, a1.username DESC;
                """, [user, channel])
            rank_data = cur.fetchone()
            return rank_data


if __name__ == "__main__":
    channel = "testchannel"
    db = Database("test.db")
    db.initiate()
    db.add_user(test_users, channel)
    print db.get_user()
    db.modify_points()
    print db.get_user()
    db.add_command()
    db.increment_command()
    print db.get_command()
    db.increment_command()
    db.modify_command()
    print db.get_command()
    db.increment_command()
    print db.get_command()
    db.add_quote()
    print db.get_quote()
    raw_input("press enter to delete the test entries")
    db.remove_command()
    for user in test_users:
        db.remove_user(user)
    db.remove_quotes()
