import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import csv


def predict_breed(adaptability, energy, friendliness, health_grooming, trainability, size):
    # bring in csv file
    breeds = pd.read_csv('baseapp/datasets/breedparameterdata with labels.csv')
    # Delete breed names from breeds
    del breeds['Breeds Names']
    # Pre process
    # Create empty arrays
    breed_id = []
    breed_names = []
    # get csv file data with out headers
    csv_file_path = 'baseapp/datasets/breedparameterdata.csv'
    with open(csv_file_path, encoding='utf8') as f:
        reader = csv.reader(f)
        # Read through each row add breed names into array
        for row in reader:
            breed_names.append(row[1])
    # Fill breed id array
    for x in range(213):
        breed_id.append(x)

    breeds['Breed'] = pd.cut(breeds['Breed'], bins=213, labels=breed_id)
    label_breed = LabelEncoder()
    breeds['Breed'] = label_breed.fit_transform(breeds['Breed'])
    x = breeds.drop('Breed', 1)
    y = breeds['Breed']
    # Scale
    sc = StandardScaler()
    x = sc.fit_transform(x)
    # Create RandomForest
    rfc = RandomForestClassifier(n_estimators=200)
    rfc.fit(x, y)

    # Get values to predict
    to_predict = [[adaptability, energy, friendliness, health_grooming, trainability, size]]
    # Scale values to predict
    to_predict = sc.transform(to_predict)
    # Predict for all breeds
    id_all_predicted = rfc.predict_proba(to_predict)[0]
    # Get the top five closest match
    predicted_array = first_five(merge(breed_names, id_all_predicted))
    return predicted_array


# merge two arrays to create array of tuples
def merge(array1, array2):
    merged = [(array1[i], array2[i]) for i in range(0, 213)]
    return merged


# get sorting key
def get_key(item):
    return item[1]


# sort by accuracy and return top 5 names
def first_five(array):
    # Sort
    sorted_array = sorted(array, key=get_key, reverse=True)
    top_five = []
    # Get top 5
    for i in range(5):
        top_five.append(sorted_array[i][0])
    return top_five
