import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', None)
# Load training data
# To run, aspeed must be in same directory
data = pd.read_csv('aspeed.csv')
#data = pd.read_csv('baseapp/datasets/aspeed.csv')

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


# Correlation Heatmap
sns.heatmap(data.corr(), annot=True)
plt.show()


print("Data Describe")
print(data.describe().T)
print("Unique values in columns")
print(data.nunique())
print("Null values in columns")
print(data.isnull().sum())
print("Data head")
print(data.head())


# Preprocess
x = data.drop('AdoptionSpeed', 1)
y = data['AdoptionSpeed']

# Scale/Normalize
sc = StandardScaler()
sc.fit(x)
x_lr = sc.fit_transform(x)
# Apply logistic regression
lr = LogisticRegression()
lr.fit(x_lr, y)
importance = lr.coef_[0]
plt.bar([x for x in range(len(importance))], importance)
plt.show()

# Drop low relevance columns
data = data.drop(['Breed1', 'FurLength', 'Vaccinated', 'Sterilized'], axis=1)
print(data.head())
x = data.drop('AdoptionSpeed', 1)
y = data['AdoptionSpeed']
# Spilt Data -> train & test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=40)
# Scale/Normalize
sc = StandardScaler()
sc.fit(x_train)
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Prediction modeling
gnb = GaussianNB()
gnb.fit(x_train, y_train)
predict_gnb = gnb.predict(x_test)
accuracy = accuracy_score(y_test, predict_gnb)


# Print results
print("Classification Report")
print(classification_report(y_test, predict_gnb))
print("Confusion Matrix")
print(confusion_matrix(y_test, predict_gnb))
print("Accuracy")
print(round(accuracy*100, 2))
sns.heatmap(confusion_matrix(y_test, predict_gnb), annot=True, fmt='g')
plt.show()




