import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB


def predict_speed(age, gender, size, fur_length, vaccinated, dewormed, sterilized, health):
    adoption_speed = pd.read_csv('aspeed.csv')

    adoption_speed = adoption_speed[adoption_speed.Type != 2]
    del adoption_speed['Type']
    del adoption_speed['Id']
    adoption_speed = adoption_speed[adoption_speed.Quantity == 1]
    del adoption_speed['Quantity']
    del adoption_speed['Breed1']
    del adoption_speed['Breed2']
    del adoption_speed['Fee']
    del adoption_speed['Color1']
    del adoption_speed['Color2']
    del adoption_speed['Color3']

    X = adoption_speed.drop('AdoptionSpeed', 1)
    y = adoption_speed['AdoptionSpeed']

    sc = StandardScaler()
    X = sc.fit_transform(X)

    gnb = GaussianNB()
    gnb.fit(X, y)

    to_predict = [[age, gender, size, fur_length, vaccinated, dewormed, sterilized, health]]
    to_predict = sc.transform(to_predict)
    adpotion_speed_predicted = gnb.predict(to_predict)
    return adpotion_speed_predicted

