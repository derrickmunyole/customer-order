
import time
from django.core.management import BaseCommand

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Command to wait for the database"""
    def handle(self, *args, **options):
        """Command Entrypoint"""
        self.stdout.write('Waiting for database to start...')
        is_db_up = False

        while is_db_up is False:
            try:
                self.check(databases=['default'])
                is_db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable. Waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
