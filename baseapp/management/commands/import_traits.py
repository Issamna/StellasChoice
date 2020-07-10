# run with `python manage.py import_traits`

from django.core.management.base import BaseCommand
import csv
from baseapp.models import Breed
from django.conf import settings


class Command(BaseCommand):


    help = 'Re-run receipt status update for all receipts'

    def handle(self, *args, **options):
        if settings.DEBUG:
            csv_file_path = 'baseapp/datasets/breedparameterdata.csv'
            with open(csv_file_path, encoding='utf8') as f:
                reader = csv.reader(f)
                for row in reader:
                    breed = Breed.objects.get_or_create(name=row[1])[0]
                    breed.adaptability = row[2]
                    breed.energy = row[3]
                    breed.friendliness = row[4]
                    breed.health_grooming = row[5]
                    breed.trainability = row[6]
                    breed.size = row[7]
                    breed.save()

            Breed.objects.filter(friendliness=0).delete()


