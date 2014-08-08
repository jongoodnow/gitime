import gitime.database as db
import gitime.invoice as invoice
import gitime.user as user
import unittest
import sqlite3
import os

class TestInvoice(unittest.TestCase):

    def setUp(self):
        db.DB_NAME = 'test.db'
        db.first_time_setup()
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()
        self.user = user.User()

    def tearDown(self):
        self.conn.close()
        os.remove('test.db')

    def test_create_invoice(self):
    	inv = invoice.Invoice('some project', new=True, rate=20.0, rounding=1.0)
    	self.c.execute('SELECT * FROM invoice WHERE name="some project"')
    	self.assertEqual(self.c.fetchone(), ('some project', 20.0, 1.0))

    def test_access_invoice(self):
    	db.insert_invoice('a project', 20.0, 1.0)
    	inv = invoice.Invoice('a project')
    	self.assertEqual(inv.name, 'a project')
    	self.assertEqual(inv.rate, 20.0)
    	self.assertEqual(inv.rounding, 1.0)

    def test_total_earnings(self):
    	invid = db.insert_invoice('a project', 20.0, 1.0)
    	db.insert_commit('fixed a thing', 1405287929, 2, invid)
    	inv = invoice.Invoice(invid)
    	self.assertEqual(inv.total_earnings(), 40.0)