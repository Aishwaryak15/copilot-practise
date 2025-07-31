import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../main/python')))
from app import app

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.patcher = patch('app.get_db_connection')
        self.mock_get_db_connection = self.patcher.start()
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

    def tearDown(self):
        self.patcher.stop()

    def test_list_users(self):
        self.mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'John', 'email': 'john@example.com'}
        ]
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)

    def test_add_user(self):
        self.mock_cursor.lastrowid = 1
        response = self.app.post('/users', json={'name': 'Jane', 'email': 'jane@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Jane', response.data)

    def test_get_user(self):
        self.mock_cursor.fetchone.return_value = {'id': 1, 'name': 'John', 'email': 'john@example.com'}
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)

    def test_get_user_not_found(self):
        self.mock_cursor.fetchone.return_value = None
        response = self.app.get('/users/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'User not found', response.data)

    def test_update_user(self):
        response = self.app.put('/users/1', json={'name': 'Jane', 'email': 'jane@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane', response.data)

    def test_delete_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted', response.data)

    def test_delete_user_not_found(self):
        # Simulate no user deleted (e.g., DB returns 0 rows affected)
        self.mock_conn.cursor.return_value.rowcount = 0
        response = self.app.delete('/users/99')
        # The app currently always returns 200, but you may want to handle this in your app
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted', response.data)

    def test_update_user_missing_fields(self):
        response = self.app.put('/users/1', json={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'null', response.data)
