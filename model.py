import numpy as np
import pandas as pd
import pickle

titanic_train = pd.read_csv('./train.csv')
titanic_train = titanic_train.drop(['Ticket', 'Cabin'], axis=1)
titanic_train['Title'] = titanic_train.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

titanic_train['Title'] = titanic_train['Title'].replace(['Lady', 'Countess','Capt', 'Col',\
 	'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

titanic_train['Title'] = titanic_train['Title'].replace('Mlle', 'Miss')
titanic_train['Title'] = titanic_train['Title'].replace('Ms', 'Miss')
titanic_train['Title'] = titanic_train['Title'].replace('Mme', 'Mrs')

title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}

titanic_train['Title'] = titanic_train['Title'].map(title_mapping)
titanic_train['Title'] = titanic_train['Title'].fillna(0)
titanic_train = titanic_train.drop(['Name', 'PassengerId'], axis=1)
titanic_train['FamilySize'] = titanic_train['SibSp'] + titanic_train['Parch'] + 1

titanic_train['IsAlone'] = 0
titanic_train.loc[titanic_train['FamilySize'] == 1, 'IsAlone'] = 1


features = ["Pclass", "Sex", "IsAlone","Age", "Embarked", 'Title']
titanic_train.Age = titanic_train.Age.fillna(titanic_train.Age.median())

X = pd.get_dummies(titanic_train[features])

y = titanic_train["Survived"]

print(X.head())


#from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
#scaler=StandardScaler()
#scaler.fit(X)

#X_train_scaled = scaler.transform(X)
#print(X_train_scaled)

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X, y)
random_forest.score(X, y)
acc_random_forest = round(random_forest.score(X, y) * 100, 2)
print(acc_random_forest)


pickle.dump(random_forest, open('model.pickle','wb'))