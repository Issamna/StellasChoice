# run with `python manage.py import_breeds`
from django.core.management.base import BaseCommand
import csv
from baseapp.models import Breed
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Inserts breed labels'

    def handle(self, *args, **options):
        # Only possible in dev mode
        if settings.DEBUG:
            # Truncate all previous data
            with connection.cursor() as cursor:
                cursor.execute("delete from baseapp_breed", [])
            # get csv file data
            csv_file_path = "baseapp/datasets/breed_labels.csv"
            with open(csv_file_path) as f:
                reader = csv.reader(f)
                # Read through each row
                for row in reader:
                    # Must be type dog
                    if row[1] == '1':
                        # Create breed and insert to DB
                        breed = Breed.objects.get_or_create(name=row[2], csv_id=row[0])
