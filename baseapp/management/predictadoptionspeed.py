import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB


def predict_speed(age, breed2, gender, size, dewormed, health):

    data = pd.read_csv('baseapp/datasets/aspeed.csv')

    # Remove Cat Data
    data = data[data.Type != 2]
    # Remove Dogs with quantity greater than 1
    data = data[data.Quantity == 1]
    # Drop unnecessary columns
    data = data.drop(['Type', 'Quantity', 'Name', 'Color1', 'Color2', 'Color3', 'Fee', 'State',
                      'RescuerID', 'VideoAmt', 'Description', 'PetID', 'PhotoAmt'], axis=1)

    # Remove where breed1 equals 0 or 307
    data = data[data.Breed1 != 0]
    data = data[data.Breed1 != 307]
    # if Breed1 matches Breed2 change Breed2 -> 0
    data.loc[data['Breed1'] == data['Breed2'], ['Breed2']] = 0
    # Remove where column equals 3 for health attributes
    data = data[data.Vaccinated != 3]
    data = data[data.Dewormed != 3]
    data = data[data.Sterilized != 3]
    # Convert 1 -> 0 and 2 -> 1
    data.loc[data['Gender'] == 1, ['Gender']] = 0
    data.loc[data['Gender'] == 2, ['Gender']] = 1
    data.loc[data['Vaccinated'] == 1, ['Vaccinated']] = 0
    data.loc[data['Vaccinated'] == 2, ['Vaccinated']] = 1
    data.loc[data['Dewormed'] == 1, ['Dewormed']] = 0
    data.loc[data['Dewormed'] == 2, ['Dewormed']] = 1
    data.loc[data['Sterilized'] == 1, ['Sterilized']] = 0
    data.loc[data['Sterilized'] == 2, ['Sterilized']] = 1
    # Breed2 anything not 0 change to 1
    data.loc[data['Breed2'] > 0, ['Breed2']] = 1
    # Change adoption speed to reflect less than or greater than 30 days
    data.loc[data['AdoptionSpeed'] == 1, ['AdoptionSpeed']] = 0
    data.loc[data['AdoptionSpeed'] == 2, ['AdoptionSpeed']] = 0
    data.loc[data['AdoptionSpeed'] == 3, ['AdoptionSpeed']] = 1
    data.loc[data['AdoptionSpeed'] == 4, ['AdoptionSpeed']] = 1

    # Drop low relevance columns
    data = data.drop(['Breed1', 'FurLength', 'Vaccinated', 'Sterilized'], axis=1)

    x = data.drop('AdoptionSpeed', 1)
    y = data['AdoptionSpeed']

    sc = StandardScaler()
    sc.fit(x)
    x = sc.fit_transform(x)
    # Apply Naive Bayes
    gnb = GaussianNB()
    gnb.fit(x, y)
    # Predict
    to_predict = [[age, breed2, gender, size, dewormed, health]]
    to_predict = sc.transform(to_predict)
    adoption_speed_predicted = gnb.predict(to_predict)
    return adoption_speed_predicted[0]
