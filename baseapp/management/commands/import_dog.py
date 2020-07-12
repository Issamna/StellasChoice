# run with `python manage.py import_dog`

from django.core.management.base import BaseCommand
import csv
from baseapp.models import Dog
from baseapp.models import Breed
from django.db import connection
from django.conf import settings
from baseapp.management.predictadoptionspeed import predict_speed


class Command(BaseCommand):
    help = 'Inserts initial adoptable dog list'

    def handle(self, *args, **options):
        # Only possible in dev mode
        if settings.DEBUG:
            # Truncate all previous data
            with connection.cursor() as cursor:
                cursor.execute("delete from baseapp_dog", [])
            # get csv file data
            csv_file_path = "baseapp/datasets/test.csv"
            with open(csv_file_path, encoding='utf8') as f:
                reader = csv.reader(f)
                # Read through each row
                for row in reader:
                    # Must be type dog
                    if row[0] == '1':
                        # Get matching breed from Breed table
                        breed_one = Breed.objects.filter(csv_id=row[3])
                        breed_two = Breed.objects.filter(csv_id=row[4])
                        # Checks if breed two exists
                        if len(breed_two) >= 1:
                            # Assign breed two
                            breed_two = breed_two[0]
                        else:
                            # Creates null value if doesn't
                            breed_two = None
                        # Checks if breed one exists
                        if len(breed_one) >= 1:
                            # Assign breed one
                            breed_one = breed_one[0]
                            # Create dog and insert to DB
                            dog = Dog.objects.create(
                                pet_id=row[21],
                                name=row[1],
                                age=row[2],
                                breed_one=breed_one,
                                breed_two=breed_two,
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
                                # Predict speed using parameters
                                adoption_speed=predict_speed(row[2], row[5], row[9], row[10],
                                                             row[11], row[13], row[14])
                            )
