from __future__ import unicode_literals
import gitime.database as db
import gitime.invoice as invoice
import gitime.commit as commit
import gitime.user as user
import unittest
import sqlite3
import os

class TestCommit(unittest.TestCase):

    def setUp(self):
        db.DB_NAME = 'test.db'
        db.first_time_setup()
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()
        self.user = user.User()
        self.inv = invoice.Invoice('some project', new=True, rate=20.0, rounding=1.0)

    def tearDown(self):
        self.conn.close()
        os.remove('test.db')

    def test_create_commit(self):
        com = commit.Commit('fixed a thing', 2, 'some project')
        self.assertEqual(com.message, 'fixed a thing')
        self.assertEqual(com.hours, 2)
        self.assertEqual(com.invoice.name, 'some project')
        self.assertEqual(com.rowid, 1)

    def test_access_commit(self):
        comid = db.insert_commit('fixed a thing', 1405287929, 2, 1)
        com = commit.Commit.access(comid)
        self.assertEqual(com.message, 'fixed a thing')
        self.assertEqual(com.hours, 2)
        self.assertEqual(com.date, 1405287929)
        self.assertEqual(com.invoice.name, 'some project')
        self.assertEqual(com.rowid, comid)

    def test_parse_hours_flag(self):
        args = ['commit', '-m', 'fooed a bar', '--hours', '3']
        self.assertEqual(commit.parse_hours_flag(args), 3.0)
        self.assertEqual(args, ['commit', '-m', 'fooed a bar'])
        self.assertEqual(commit.parse_hours_flag(args), False)
        self.assertEqual(args, ['commit', '-m', 'fooed a bar'])

    def test_parse_commit_message(self):
        self.assertEqual(commit.parse_commit_message(['git', 'commit', '-am', 'did a thing']),
            'did a thing')
        self.assertEqual(commit.parse_commit_message(['git', 'commit', '-mq', 'didn\\\'t do a thing', '--short']),
            'didn\\\'t do a thing')
        self.assertEqual(commit.parse_commit_message(['git', 'commit', '-a', '--message', 'did a thing']),
            'did a thing')
        self.assertEqual(commit.parse_commit_message(['git', 'commit', '-a', "--message='didn\\\'t do a thing'"]),
            'didn\\\'t do a thing')
        args = ['git', 'commit', '-m', 'did "a t\\"hing']
        commit.parse_commit_message(args)
        self.assertEqual(args, ['git', 'commit', '-m', '"did \\"a t\\"hing"'])