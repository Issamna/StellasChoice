# run with `python manage.py testalgorithm`

from django.core.management.base import BaseCommand
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
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


class Command(BaseCommand):

    def handle(self, *args, **options):
        # print('hi')
        pets = pd.read_csv('baseapp/datasets/train/trainv2.csv')
        bins = (5)
        group_names = ['S0', 'S1', 'S2', 'S3','S4']
        pets['AdoptionSpeed'] = pd.cut(pets['AdoptionSpeed'], bins=bins, labels=group_names)
        label_quality = LabelEncoder()
        pets['AdoptionSpeed'] = label_quality.fit_transform(pets['AdoptionSpeed'])
        print(pets['AdoptionSpeed'].value_counts())
        X = pets.drop('AdoptionSpeed', axis=1)
        y = pets['AdoptionSpeed']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)


        # NB
        gnb = GaussianNB()
        gnb.fit(X_train, y_train)
        pred_gnb = gnb.predict(X_test)
        cm = accuracy_score(y_test, pred_gnb)
        print(classification_report(y_test, pred_gnb))
        print(confusion_matrix(y_test, pred_gnb))
        print(cm)
        sns.heatmap(confusion_matrix(y_test, pred_gnb))
        plt.show()


