# run with `python manage.py import_dog`

from django.core.management.base import BaseCommand
import csv
from baseapp.models import Dog
from baseapp.models import Breed
from django.db import connection
from django.conf import settings
from baseapp.management.predictadoptionspeed import predict_speed


class Command(BaseCommand):
    help = 'Re-run receipt status update for all receipts'

    def handle(self, *args, **options):

        # FOR dev
        if settings.DEBUG:

            with connection.cursor() as cursor:
                cursor.execute("delete from baseapp_dog", [])

            csv_file_path = "baseapp/datasets/test.csv"
            with open(csv_file_path, encoding='utf8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == '1':
                        breed_one = Breed.objects.filter(csv_id=row[3])
                        if len(breed_one) >= 1:
                            breed_one = breed_one[0]
                            dog = Dog.objects.create(
                                pet_id=row[21],
                                name=row[1],
                                age=row[2],
                                breed_one=breed_one,
                                breed_two=row[4],
                                gender=row[5],
                                maturity_size=row[9],
                                fur_length=row[10],
                                vaccinated=row[11],
                                dewormed=row[12],
                                sterilized=row[13],
                                health=row[14],
                                quantity=row[15],
                                fee=row[16],
                                description=row[20],
                                adoption_speed=predict_speed(row[2], row[5], row[9], row[10],
                                                             row[11], row[13], row[14])
                            )
