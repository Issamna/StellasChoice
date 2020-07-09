import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder


def predict_breed(adaptability, energy, friendliness, health_grooming, trainability, size,):
    # bring in csv file
    breeds = pd.read_csv('baseapp/datasets/breedparameterdata with labels.csv')

    # Pre process
    bins = 213
    breed_id = []
    for x in range(213):
        breed_id.append(x)
    del breeds['Breeds']

    breeds['BreedID'] = pd.cut(breeds['BreedID'], bins=bins, labels=breed_id)
    label_quality = LabelEncoder()
    breeds['BreedID'] = label_quality.fit_transform(breeds['BreedID'])
    X = breeds.drop('BreedID', 1)
    Y = breeds['BreedID']

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

    predicted_array = first_five(merge(breed_id, id_all_predicted))
    return predicted_array


def merge(array1, array2):
    merged = [[array1[i], array2[i]] for i in range(0, 213)]
    return merged


def get_key(item):
    return item[1]


def first_five(array):
    sorted_array = sorted(array, key=get_key, reverse=True)
    top_five = []
    for i in range(5):
        top_five.append(sorted_array[i][0])
    return top_five




