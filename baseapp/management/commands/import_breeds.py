# run with `python manage.py import_breeds`

from django.core.management.base import BaseCommand
import csv
from baseapp.models import Breed
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Re-run receipt status update for all receipts'

    def handle(self, *args, **options):

        # FOR dev
        if settings.DEBUG:

            with connection.cursor() as cursor:
                cursor.execute("delete from baseapp_breed", [])

            csv_file_path = "baseapp/datasets/breed_labels.csv"

            with open(csv_file_path) as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[1] == '1':
                        breed = Breed.objects.get_or_create(name=row[2], csv_id=row[0])

            breed = Breed.objects.get_or_create(name='Unknown', csv_id=9999)