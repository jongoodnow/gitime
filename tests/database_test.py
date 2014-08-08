import gitime.database as db
import unittest
import sqlite3
import os

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.DB_NAME = 'test.db'
        db.first_time_setup()
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        os.remove('test.db')

    def test_new_database(self):
        self.c.execute('SELECT * FROM user')
        self.assertEqual(self.c.fetchall(), [(0.0, 0.25, 0, 0, 0, 0)])
        self.c.execute('SELECT * FROM invoice')
        self.assertEqual(self.c.fetchall(), [])
        self.c.execute('SELECT * FROM gtcommit')
        self.assertEqual(self.c.fetchall(), [])

    def test_insert(self):
        invoice_id = db.insert_invoice('Cool Project', 20.0, 1.0)
        self.c.execute('SELECT * FROM invoice WHERE rowid=?', (invoice_id,))
        self.assertEqual(self.c.fetchall(), [('Cool Project', 20.0, 1.0)])
        commit_id = db.insert_commit('Did a thing', 1405184155, 2.0, invoice_id)
        self.c.execute('SELECT * FROM gtcommit WHERE commit_invoice=?', (invoice_id,))
        self.assertEqual(self.c.fetchall(), [('Did a thing', 1405184155, 2.0, invoice_id)])

    def test_query(self):
        invoice_id = db.insert_invoice('Cool Project', 20.0, 1.0)
        commit_id = db.insert_commit('Did a thing', 1405184155, 2.0, invoice_id)
        self.assertEqual(db.query_user(1), (0.0, 0.25, 0, 0, 0, 0))
        self.assertEqual(db.query_invoice(1), ('Cool Project', 20.0, 1.0))
        self.assertEqual(db.query_invoice('Cool Project'), ('Cool Project', 20.0, 1.0, 1))
        self.assertEqual(db.query_commit(1), ('Did a thing', 1405184155, 2.0, invoice_id))
        self.assertEqual(db.query_invoice_commit_meta(1), [('Did a thing', 1405184155, 2.0, invoice_id)])

    def test_update(self):
        invoice_id = db.insert_invoice('Cool Project', 20.0, 1.0)
        db.update(lambda c_: c_.execute('UPDATE invoice SET rate=? WHERE rowid=?', (40.0, invoice_id)))
        self.c.execute('SELECT * FROM invoice WHERE rowid=?', (invoice_id,))
        self.assertEqual(self.c.fetchall(), [('Cool Project', 40.0, 1.0)])