
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2rror

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test suite for database connection management commands.
    Inherits from SimpleTestCase for testing without database access.
    """

    def test_db_ready_state(self, patched_check):
        """
        Test case to verify behavior when database is immediately ready.

        Args:
            patched_check: Mock object that simulates database connection
            checking

        Tests:
            - Verifies that wait_for_db command executes successfully when DB
              is ready
            - Ensures check is called exactly once with the default database
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test case to verify retry behavior when database connection fails
        initially.

        Args:
            patched_sleep: Mock object that simulates time.sleep to avoid
                           actual delays
            patched_check: Mock object that simulates database connection
                           checking

        Test Scenario:
            - First 2 attempts raise Psycopg2Error (database service not ready)
            - Next 3 attempts raise OperationalError (database ready but not
              accepting connections)
            - Final attempt succeeds

        Tests:
            - Verifies command retries appropriate number of times
            - Confirms total number of attempts equals 6
            - Ensures final check is made against the default database
        """
        patched_check.side_effect = [Psycopg2rror] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)

        patched_check.assert_called_with(databases=['default'])
