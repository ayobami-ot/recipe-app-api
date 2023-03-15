"""
Django comand to wait for database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.db import connection, OperationalError


class Command(BaseCommand):
    help = 'Django command to wait for database'

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                connection.ensure_connection()
                db_up = True
            except OperationalError as e:
                self.stdout.write(f'Database unavailable: {str(e)}')
                self.stdout.write('Waiting 1 second before retrying...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
