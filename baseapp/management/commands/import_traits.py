# run with `python manage.py import_breeds`

from django.core.management.base import BaseCommand
import json
from baseapp.models import Breed
from django.db import connection
from django.conf import settings


class Command(BaseCommand):


    help = 'Re-run receipt status update for all receipts'

    def handle(self, *args, **options):

        with open('baseapp/datasets/rating.json') as f:
            data = json.load(f)
            for dogbreed in data['dog_breeds']:
                friendliness_import = 0
                exercise_needs_import = 0
                trainability_import = 0
                apartment_living_import = 0
                affectionate_with_family_import = 0
                groom_import = 0
                energy_import = 0
                _import = 0
                sensitivity_lvl_import = 0
                size_import = 0
                bark_howl_tendency_import = 0
                being_alone_import = 0
                try:
                    dogbreed_data = data['dog_breeds'][dogbreed]
                    friendliness_import = dogbreed_data[' All Around Friendliness']
                    exercise_needs_import = dogbreed_data[' Exercise Needs']
                    trainability_import = dogbreed_data[' Trainability']
                    apartment_living_import = dogbreed_data['Adapts Well to Apartment Living']
                    affectionate_with_family_import = dogbreed_data['Affectionate with Family']
                    groom_import = dogbreed_data['Easy To Groom']
                    energy_import = dogbreed_data['Energy Level']
                    intelligence_import = dogbreed_data['Intelligence']
                    sensitivity_lvl_import = dogbreed_data['Sensitivity Level']
                    size_import = dogbreed_data['Size']
                    bark_howl_tendency_import = dogbreed_data['Tendency To Bark Or Howl']
                    being_alone_import = dogbreed_data['Tolerates Being Alone']
                except KeyError:
                    print("Oops!  That was no valid key.  Try again...")
                breed = Breed.objects.get_or_create(name=dogbreed)[0]
                breed.friendliness = friendliness_import
                breed.exercise_needs = exercise_needs_import
                breed.trainability = trainability_import
                breed.apartment_living = apartment_living_import
                breed.affectionate_with_family = affectionate_with_family_import
                breed.groom = groom_import
                breed.energy = energy_import
                breed.intelligence = intelligence_import
                breed.sensitivity_lvl = sensitivity_lvl_import
                breed.size = size_import
                breed.bark_howl_tendency = bark_howl_tendency_import
                breed.being_alone = being_alone_import
                breed.save()

