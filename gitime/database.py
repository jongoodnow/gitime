import sqlite3

DB_NAME = 'gitime.db'

def first_time_setup():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.executescript("""
            DROP TABLE IF EXISTS user;
            DROP TABLE IF EXISTS invoice;
            DROP TABLE IF EXISTS gtcommit;
            CREATE TABLE user(
                rate           REAL    DEFAULT 0       NOT NULL,
                rounding       REAL    DEFAULT 1       NOT NULL,
                timer_running  INTEGER DEFAULT 0       NOT NULL,
                timer_start    INTEGER DEFAULT 0       NOT NULL,
                timer_total    INTEGER DEFAULT 0       NOT NULL,
                active_invoice INTEGER,
                FOREIGN KEY(active_invoice) REFERENCES invoice(rowid)
            );
            CREATE TABLE invoice(
                name           TEXT    DEFAULT ''      NOT NULL,
                rate           REAL    DEFAULT 0       NOT NULL,
                rounding       REAL    DEFAULT 1       NOT NULL
            );
            CREATE TABLE gtcommit(
                message        TEXT    DEFAULT ''      NOT NULL,
                date           INTEGER DEFAULT 0       NOT NULL,
                hours          REAL    DEFAULT 0       NOT NULL,
                commit_invoice INTEGER,
                FOREIGN KEY(commit_invoice) REFERENCES invoice(rowid)
            );
            INSERT INTO user DEFAULT VALUES;
        """)
        conn.commit()
    except sqlite3.Error as e:
        print "Database Error: %s" %e.args[0]
    finally:
        if conn:
            conn.close()

def query(table, rows='*', where=None, fetchone=False):
    conn = None
    results = None
    where_clause = ''
    if where:
        where_clause = ' '.join(['WHERE', ' AND '.join('%s:%s' %(key, val) for (key, val) in where.iteritems())])
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT ? FROM ? ?", (rows, table, where_clause))
        results = c.fetchone() if fetchone else c.fetchall()
    except sqlite3.Error as e:
        print "Database Error: %s" %e.args[0]
    finally:
        if conn:
            conn.close()
    return results