import gitime.database as db
import gitime.user as user
import time
import unittest
import sqlite3
import os

class TestUser(unittest.TestCase):

    def setUp(self):
        db.DB_NAME = 'test.db'
        db.first_time_setup()
        self.user = user.User()
        # make the time static so we can test it
        user.unix_now = lambda: 1405287929

    def tearDown(self):
        os.remove('test.db')

    def test_timer_init(self):
        self.assertEqual(self.user.timer_running, False)
        self.assertEqual(self.user.timer_start, 0)
        self.assertEqual(self.user.timer_total, 0)        

    def test_timer_start(self):
        self.user.start_timer()
        self.assertEqual(self.user.timer_running, True)
        self.assertEqual(self.user.timer_start, 1405287929)

    def test_timer_reset(self):
        self.user.start_timer()
        self.user.reset_timer()
        self.assertEqual(self.user.timer_running, False)
        self.assertEqual(self.user.timer_start, 0)
        self.assertEqual(self.user.timer_total, 0)

    def test_timer_pause(self):
        self.user.start_timer()
        user.unix_now = lambda: 1405291529
        self.user.pause_timer()
        self.assertEqual(self.user.time_tracked(), 1)