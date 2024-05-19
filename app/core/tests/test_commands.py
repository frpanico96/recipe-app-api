"""
Test custom Django management commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Providing the path that we want to mock with @patch decorator
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """
    Test commands
    """

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database if database ready
        """
        patched_check.return_value = True

        call_command('wait_for_db')
        # this line ensure that the command is called with default db
        patched_check.assert_called_once_with(databases=['default'])

    # Mock the sleep between two calls to the db
    # Arguments appears in the order
    # From the innermost patch to the outermost
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when getting OperationalError
        It throws 2 Psycopg error and 3 OperationalError
        Then returns true
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        # Check the command is called only 6 times
        # and the db is called with the default db
        self.assertEqual(patched_check.call_count, 6,
                         "Incorrect number of db calls")
        patched_check.assert_called_with(databases=['default'])
