import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import csv

def predict_breed(adaptability, energy, friendliness, health_grooming, trainability, size):
    # bring in csv file
    breeds = pd.read_csv('baseapp/datasets/breedparameterdata with labels.csv')
    del breeds['Breeds Names']
    # Pre process
    bins = (213)
    breed_id = []
    breed_names = []
    csv_file_path = 'baseapp/datasets/breedparameterdata.csv'
    with open(csv_file_path, encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            breed_names.append(row[1])
    for x in range(213):
        breed_id.append(x)
    breeds['Breed'] = pd.cut(breeds['Breed'], bins=bins, labels=breed_id)
    label_quality = LabelEncoder()
    breeds['Breed'] = label_quality.fit_transform(breeds['Breed'])
    X = breeds.drop('Breed', 1)
    Y = breeds['Breed']

    # Scale
    sc = StandardScaler()
    X = sc.fit_transform(X)

    # Create RandomForest
    rfc = RandomForestClassifier(n_estimators=200)
    rfc.fit(X, Y)

    to_predict = [[adaptability, energy, friendliness, health_grooming, trainability, size]]
    to_predict = sc.transform(to_predict)
    id_predicted = rfc.predict(to_predict)
    id_all_predicted = rfc.predict_proba(to_predict)[0]

    predicted_array = first_five(merge(breed_names, id_all_predicted))
    return predicted_array


def merge(array1, array2):
    merged = [(array1[i], array2[i]) for i in range(0, 213)]
    return merged


def get_key(item):
    return item[1]


def first_five(array):
    sorted_array = sorted(array, key=get_key, reverse=True)
    top_five = []
    for i in range(5):
        top_five.append(sorted_array[i][0])
    return top_five

