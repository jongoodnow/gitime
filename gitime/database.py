from __future__ import unicode_literals, print_function
import sqlite3
import sys
import os
import stat

# hack to get python 3 to not break when unicode is used
try:
    unicode
except NameError:
    unicode = str

# locate the database
DB_DIR = os.path.expanduser('~/.gitime')
PATHCHAR = '\\' if os.name == 'nt' else '/'
DB_NAME = PATHCHAR.join((DB_DIR, 'gitime.db'))


def set_unix_permissions(path):
    """ Linux and Mac users might install using sudo,
        so the user needs to be granted read and write access
        to the database
    """
    import pwd
    uname = os.getenv("SUDO_USER") or os.getenv("USER")
    os.chown(path, pwd.getpwnam(uname).pw_uid, pwd.getpwnam(uname).pw_gid)
    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


def db_exists():
    return os.path.isfile(DB_NAME)


def _db_connect(action, new_db=False):
    """ Connects to the database, does something, and closes.
        Should only be called in `database.py`.
        Args:
        * action - a function with args 
                   (database connection object, database cursor)
        Opts:
        * new_db - if true, don't confirm that the database exists
    """
    if not new_db and not db_exists():
        print("Your database can't be found. Reinstalling should fix this.",
            file=sys.stderr)
        sys.exit()
    conn = results = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        results = action(conn, c)
    except sqlite3.Error as e:
        raise
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
                rate            REAL     DEFAULT 0     NOT NULL,
                rounding        REAL     DEFAULT 0.25  NOT NULL,
                timer_running   INTEGER  DEFAULT 0     NOT NULL,
                timer_start     INTEGER  DEFAULT 0     NOT NULL,
                timer_total     INTEGER  DEFAULT 0     NOT NULL,
                active_invoice  INTEGER  DEFAULT 0     NOT NULL,
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
                commit_invoice  INTEGER  DEFAULT 0  NOT NULL,
                FOREIGN KEY(commit_invoice) REFERENCES invoice(rowid)
            );
            INSERT INTO user DEFAULT VALUES;
        """)
        conn.commit()

    _db_connect(setup_action, True)
    if os.name in ('posix', 'mac'):
        set_unix_permissions(DB_NAME)


def _insert(statement):
    """ Runs a execute command. It should be a INSERT statment. """

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


def _query(statement, fetchall=True):
    """ Runs an execute command. It should be a SELECT statement.
        opts:
        * fetchall - in most cases, fetchall should be True because it cannot
                     be known for sure that there is only one result. But queries
                     that involve a rowid are guaranteed to return one result,
                     so fetchone is a more useful command.
    """

    def query_action(conn, c):
        statement(c)
        return c.fetchall() if fetchall else c.fetchone()

    return _db_connect(query_action)


def query_user(rowid):
    return _query(lambda c: c.execute("SELECT * FROM user WHERE rowid=?", 
        (rowid,)), False)


def query_invoice(unique):
    """ invoices can be queried by either name or id. 
        Queries for names will return the rowid as the last value
    """
    if type(unique) is int:
        if unique > invoice_count():
            raise Exception("Rowid %d not in table invoice" %unique)
        return _query(lambda c: c.execute("SELECT * FROM invoice WHERE rowid=?", 
            (unique,)), False)
    elif type(unique) in (str, unicode):
        return _query(lambda c: c.execute("SELECT *, rowid FROM invoice WHERE name=?", 
            (unique,)), False)
    else:
        raise Exception("Invoice unique identifier not valid type.")


def query_commit(rowid):
    return _query(lambda c: c.execute("SELECT * FROM gtcommit WHERE rowid=?", 
        (rowid,)), False)


def query_invoice_commit_meta(rowid):
    """ List of tuples of commit metadata. """
    return _query(lambda c: c.execute("SELECT * FROM gtcommit WHERE commit_invoice=?", 
        (rowid,)))


def invoice_count():
    return _query(lambda c: c.execute("SELECT COUNT(*) FROM invoice"), False)[0]


def query_all_invoices():
    return _query(lambda c: c.execute("SELECT *, rowid FROM invoice"))


def update(statement):
    """ Runs an execute command. It should be an UPDATE statement.
        Unlike `_insert` and `_query`, this function is public because
        there is no clean and efficient way to create a general purpose
        update function. This requires raw SQL to be written outside of
        `database.py`, for this case only.
    """

    def update_action(conn, c):
        statement(c)
        conn.commit()

    _db_connect(update_action)