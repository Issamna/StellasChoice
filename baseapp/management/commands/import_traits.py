# run with `python manage.py import_traits`

from django.core.management.base import BaseCommand
import csv
from baseapp.models import Breed
from django.conf import settings


class Command(BaseCommand):
    help = 'Inserts breed traits'

    def handle(self, *args, **options):
        # Only possible in dev mode
        if settings.DEBUG:
            # get csv file data
            csv_file_path = 'baseapp/datasets/breedparameterdata.csv'
            with open(csv_file_path, encoding='utf8') as f:
                reader = csv.reader(f)
                # Read through each row
                for row in reader:
                    # Get matching breed label
                    breed = Breed.objects.get_or_create(name=row[1])[0]
                    # Update breed parameters
                    breed.adaptability = row[2]
                    breed.energy = row[3]
                    breed.friendliness = row[4]
                    breed.health_grooming = row[5]
                    breed.trainability = row[6]
                    breed.size = row[7]
                    breed.save()

            # Delete breeds with no parameter data
            Breed.objects.filter(friendliness=0).delete()


