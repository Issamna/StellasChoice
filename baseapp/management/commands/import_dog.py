# run with `python manage.py import_dog`

from django.core.management.base import BaseCommand
import csv
from baseapp.models import Dog
from baseapp.models import Breed
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Inserts initial adoptable dog list'

    def handle(self, *args, **options):
        # Only possible in dev mode
        if settings.DEBUG:
            # Truncate all previous data
            with connection.cursor() as cursor:
                cursor.execute("delete from baseapp_dog", [])
            # get csv file data
            csv_file_path = "baseapp/datasets/uploadtest.csv"
            with open(csv_file_path, encoding='utf8') as f:
                total_count = 0
                bad_count = 0
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
                            has_breed2 = 1
                        else:
                            # Creates null value if doesn't
                            breed_two = None
                            has_breed2 = 0
                        # Checks if breed one exists
                        if len(breed_one) >= 1:
                            # Assign breed one
                            breed_one = breed_one[0]

                            if row[5] == '1':
                                gender = 0
                            else:
                                gender = 1

                            if row[12] == '1':
                                dewormed = 0
                            else:
                                dewormed = 1

                            # Create dog and insert to DB
                            dog = Dog.objects.create(
                                pet_id=row[21],
                                name=row[1],
                                age=row[2],
                                breed_one=breed_one,
                                breed_two=breed_two,
                                gender=gender,
                                maturity_size=row[9],
                                vaccinated=row[11],
                                dewormed=dewormed,
                                sterilized=row[13],
                                health=row[14],

                            )
                            # debug - to see how many right and wrong
                            total_count+=1
                            if int(row[23]) != dog.adoption_speed:
                                bad_count+=1
                # debug - to see how many right and wrong
                print("results")
                print(bad_count)
                print(total_count)
