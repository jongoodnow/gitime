from __future__ import unicode_literals
from util import cache
import sqlite3
import re

DB_NAME = 'gitime.db'

def _db_connect(action):
    """ Connects to the database, does something, and closes.
        Should only be called in `database.py`.
        Args:
        * action - a function with args 
                   (database connection object, database cursor)
    """
    conn = results = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        results = action(conn, c)
    except sqlite3.Error as e:
        print "Database Error: %s" %e
    finally:
        if conn:
            conn.close()
    return results


def first_time_setup():
    """ Creates a database, or resets an existing one """

    def setup_action(conn, c):
        c.executescript("""
            DROP TABLE IF EXISTS user;
            DROP TABLE IF EXISTS invoice;
            DROP TABLE IF EXISTS gtcommit;
            CREATE TABLE user(
                rate            REAL     DEFAULT 0  NOT NULL,
                rounding        REAL     DEFAULT 1  NOT NULL,
                timer_running   INTEGER  DEFAULT 0  NOT NULL,
                timer_start     INTEGER  DEFAULT 0  NOT NULL,
                timer_total     INTEGER  DEFAULT 0  NOT NULL,
                active_invoice  INTEGER,
                FOREIGN KEY(active_invoice) REFERENCES invoice(rowid)
            );
            CREATE TABLE invoice(
                name            TEXT     DEFAULT '' NOT NULL  UNIQUE,
                rate            REAL     DEFAULT 0  NOT NULL,
                rounding        REAL     DEFAULT 1  NOT NULL
            );
            CREATE TABLE gtcommit(
                message         TEXT     DEFAULT '' NOT NULL,
                date            INTEGER  DEFAULT 0  NOT NULL,
                hours           REAL     DEFAULT 0  NOT NULL,
                commit_invoice  INTEGER,
                FOREIGN KEY(commit_invoice) REFERENCES invoice(rowid)
            );
            INSERT INTO user DEFAULT VALUES;
        """)
        conn.commit()

    _db_connect(setup_action)


def _insert(statement):

    def insert_action(conn, c):
        statement(c)
        conn.commit()
        return c.lastrowid

    return _db_connect(insert_action)


def insert_invoice(name, rate, rounding):
    return _insert(lambda c: c.execute("INSERT INTO invoice VALUES (?,?,?)", 
        (name, rate, rounding)))


def insert_commit(message, date, hours, invoice_id):
    return _insert(lambda c: c.execute("INSERT INTO gtcommit VALUES (?,?,?,?)", 
        (message, date, hours, invoice_id)))


def _query(statement):

    def query_action(conn, c):
        statement(c)
        return c.fetchall()

    return _db_connect(query_action)


def query_user(rowid):
    return _query(lambda c: c.execute("SELECT * FROM user WHERE rowid=?", (rowid,)))


def query_invoice(unique):
    """ invoices can be queried by either name or id. """
    if type(unique) is int:
        return _query(lambda c: c.execute("SELECT * FROM invoice WHERE rowid=?", (unique,)))
    elif type(unique) is str:
        return _query(lambda c: c.execute("SELECT * FROM invoice WHERE name=?", (unique,)))
    else:
        raise Exception("Invoice unique identifier not valid type.")


def query_commit(rowid):
    return _query(lambda c: c.execute("SELECT * FROM gtcommit WHERE rowid=?", (rowid,)))


def query_invoice_commits(rowid):
    return _query(lambda c: c.execute("SELECT * FROM gtcommit WHERE commit_invoice=?", (rowid,)))


def _update(statement):

    def update_action(conn, c):
        statement(c)
        conn.commit()

    _db_connect(update_action)


def update_user(rowid, rate, rounding, timer_running, timer_start, timer_total, active_invoice):
    return _update(lambda c: c.execute("""
        UPDATE user SET rate=?, rounding=?, timer_running=?, timer_start=?, timer_total=?, active_invoice=?
        WHERE rowid=?
    """, (rate, rounding, timer_running, timer_start, timer_total, active_invoice, rowid)))