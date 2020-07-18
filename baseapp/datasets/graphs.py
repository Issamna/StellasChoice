import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', None)
# Load training data
data = pd.read_csv("aspeed.csv")

# Remove Cat Data
data = data[data.Type != 2]
# Remove Dogs with quantity greater than 1
data = data[data.Quantity == 1]

# Change adoption speed
data.loc[data['AdoptionSpeed'] == 1, ['AdoptionSpeed']] = 0
data.loc[data['AdoptionSpeed'] == 2, ['AdoptionSpeed']] = 0
data.loc[data['AdoptionSpeed'] == 3, ['AdoptionSpeed']] = 1
data.loc[data['AdoptionSpeed'] == 4, ['AdoptionSpeed']] = 1

# Count by adoption speed
print(data['AdoptionSpeed'].value_counts())
data['AdoptionSpeed'].value_counts().sort_index().plot(kind='bar')
plt.title('Adoption Speed')
plt.show()


# Distribution by Age
data['Age'].plot(kind='hist')
print(data['Age'].value_counts())
plt.title('Distribution of Age (Age in Months)')
plt.show()

# Split into age groups
age_array = []
age_array += [data[data.Age <= 3]]
for i in range(3, 60, 6):
    age_in = data[data.Age > i]
    age_array += [age_in[age_in.Age <= i + 3]]
age_array += [data[data.Age > 60]]
age_adoptionSpeed = np.array([[sum(Age.AdoptionSpeed == 0), sum(Age.AdoptionSpeed == 1)] for Age in age_array])

# Add data into heat map
heatmap = []
for i in age_adoptionSpeed:
    heatmap += [i/(sum(i)) * 100]

# Plot
sns.heatmap(heatmap, annot=True)
plt.xlabel('Adoption Speed')
plt.ylabel('Animal Age')
plt.title('Adoption Speed by Age Year (Percentage)')

plt.show()

# Make label more descriptive
data.loc[data['AdoptionSpeed'] == 0, ['AdoptionSpeed']] = "Less than 30"
data.loc[data['AdoptionSpeed'] == 1, ['AdoptionSpeed']] = "More than 30"


# Remove where breed1 equals 0 or 307
data = data[data.Breed1 != 0]
data = data[data.Breed1 != 307]
# if Breed1 matches Breed2 change Breed2 -> 0
data.loc[data['Breed1'] == data['Breed2'], ['Breed2']] = 0
# Breed2 anything not 0 change to 1
data.loc[data['Breed2'] > 0, ['Breed2']] = 'Mixed Breed'
data.loc[data['Breed2'] == 0, ['Breed2']] = 'Pure Breed'


# Distribution by mixed/pure
print(data['Breed2'].value_counts())
data['Breed2'].value_counts().sort_index().plot(kind='bar')
plt.title('Pure Breed vs. Mixed Breed Count')
plt.show()

# Distribution by mixed/pure & adoption speed
mixed_graph = sns.countplot(x='Breed2', data=data, hue='AdoptionSpeed')
plt.xlabel('Breed')
plt.ylabel('Count')
plt.title('Adoption Speed for Pure Breed vs. Mixed Breed')
plt.show()








