import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder


def predict_breed(friendliness, exercise, trainability, apartment_living, affectionate, groom, energy,
                  intelligence, sensitivity, size, bark, alone):
    # bring in csv file
    breeds = pd.read_csv('baseapp/management/breedinfo.csv')

    # Pre process
    bins = (214)
    breed_id = []
    for x in range(214):
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

    to_predict = [[friendliness, exercise, trainability, apartment_living, affectionate, groom, energy,
                   intelligence, sensitivity, size, bark, alone]]
    to_predict = sc.transform(to_predict)
    id_predicted = rfc.predict(to_predict)
    id_all_predicted = rfc.predict_proba(to_predict)[0]

    predicted_array = first_five(merge(breed_id, id_all_predicted))
    return predicted_array


def merge(array1, array2):
    merged = [[array1[i], array2[i]] for i in range(0, 214)]
    return merged


def get_key(item):
    return item[1]


def first_five(array):
    sorted_array = sorted(array, key=get_key, reverse=True)
    top_five = []
    for i in range(5):
        top_five.append(sorted_array[i][0])
    return top_five


#print(predict_breed(1,1,1,1,1,1,1,1,1,1,1,1)[0][0])

