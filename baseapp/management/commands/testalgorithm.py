# run with `python manage.py testalgorithm`

from django.core.management.base import BaseCommand
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv

from baseapp.management.predictbreed import predict_breed
from baseapp.models import Breed
from django.db import connection
from django.conf import settings
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from baseapp.models import Breed


class Command(BaseCommand):

    def handle(self, *args, **options):
        breeds = predict_breed(1,5,1,2,3,5,4,1,2,3,5,1)

        result = Breed.objects.filter(csv_id__in=breeds)


        result_data = [{
            'name': Breed.name,
            'friendliness': Breed.friendliness,
            'exercise_needs': Breed.exercise_needs,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
            'name': Breed.name,
                        }
                       for entry in result]
        breeds_data_return = []
        #for x in breeds_data:
        #    print()
        print(list_result)
