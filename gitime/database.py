import sqlite3

def first_time_setup():
    conn = None
    try:
        conn = sqlite3.connect('gitime.db')
        c = conn.cursor()
        c.executescript("""
            DROP TABLE IF EXISTS user;
            DROP TABLE IF EXISTS invoice;
            DROP TABLE IF EXISTS gtcommit;
            CREATE TABLE user(
                id             INTEGER PRIMARY KEY,
                rate           REAL,
                timer_running  INTEGER,
                timer_start    INTEGER,
                active_invoice INTEGER,
                FOREIGN KEY(active_invoice) REFERENCES invoice(id)
            );
            CREATE TABLE invoice(
                id             INTEGER PRIMARY KEY,
                name           TEXT,
                rate           REAL
            );
            CREATE TABLE gtcommit(
                id             INTEGER PRIMARY KEY,
                message        TEXT,
                date           INTEGER,
                hours          REAL,
                commit_invoice INTERGER,
                FOREIGN KEY(commit_invoice) REFERENCES invoice(id)
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print "Database Error: %s" %e.args[0]
    finally:
        if conn:
            conn.close()