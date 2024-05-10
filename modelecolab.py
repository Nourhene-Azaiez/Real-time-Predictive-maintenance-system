# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import warnings
warnings.filterwarnings("ignore")

#Commande de réinitialisation pratique qui remet tous les paramètres de Matplotlib à leurs valeurs par défaut
plt.rcdefaults()

#Read dataset
data = pd.read_csv("/content/Data Sources/Système de maintenance prédictive pour les machines industrielles/predictive_maintenance.csv")

data.head(10)

"""##Feature comprehension"""

data.info()

#Rename column
data.columns = ['UDI', 'Product ID', 'Type', 'Air temperature', 'Process temperature', 'Rotational speed', 'Torque', 'Tool wear', 'Machine failure', 'Failure type']

data.describe().T

data.select_dtypes(include=['object']).describe().T

data['Failure type'].value_counts()

data['Type'].value_counts()

"""##Exploratory Data Analysis"""

num_cols = ['Air temperature', 'Process temperature', 'Rotational speed','Torque', 'Tool wear']
cat_cols = ['Type', 'Failure type']
label = 'Machine failure'

plt.figure(figsize = (12, 12))
for i, col in enumerate(num_cols):
    plt.subplot(3,2, i+1)
    sns.histplot(data, x = col, kde = True, alpha = 0.2, color = 'red', bins = 15)
plt.suptitle("Data Distributions", fontsize = 15)
plt.tight_layout()
plt.show()

plt.figure(figsize = (10, 7))
for i, col in enumerate(num_cols):
    plt.subplot(2,3, i+1)
    sns.rugplot(data, x = col, hue = label, height = 0.1)
    sns.boxplot(data, x = col, width = 0.25)
plt.suptitle("Data Distributions")
plt.tight_layout()
plt.show()

plt.figure(figsize = (10, 7))
for i, col in enumerate(num_cols):
    plt.subplot(2,3, i+1)
    sns.boxplot(data, x = label, y = col, width = 0.5)
plt.suptitle("Data Distribution in Relation to Machine Failure")
plt.tight_layout()
plt.show()

plt.figure(figsize = (6,6))
sns.heatmap(data[num_cols].corr(), square = True, annot = True, cmap = 'Blues', linewidths = 0.5)
plt.title("Heatmap Analysis")
plt.show()
#correlation entre les attributs

data.plot.hexbin(x='Air temperature', y='Process temperature', gridsize=20, cmap='Purples', figsize = (5,4))
plt.title("Hexbin Plot Between Process Temperature and Air Temperature")
plt.show()

data.plot.hexbin(x='Rotational speed', y='Torque', gridsize=30, cmap='Purples', figsize = (5,4))
plt.title("Hexbin Plot Between Torque and Rotational speed")
plt.show()

type_machine_failure = data[['Type', 'Machine failure']].pivot_table(index = 'Type', columns='Machine failure', aggfunc= lambda x: len(x), margins = True)

plt.figure(figsize=(4,4))
sns.heatmap(type_machine_failure, annot=True, fmt='g', cmap='Blues', cbar=False, linewidths=0.5)
plt.title("Type vs Machine Failure")
plt.show()

plt.figure(figsize = (7, 3))
ax = sns.countplot(data[data['Failure type'] != 'No Failure'], y = "Failure type", palette = 'tab20', order=data[data['Failure type'] != 'No Failure']['Failure type'].value_counts().index)
plt.title("Machine Failure Reasons")
ax.bar_label(ax.containers[0])
plt.show()

"""##Feature Engineering"""

data['Power'] = 2 * np.pi * data['Rotational speed'] * data['Torque'] / 60

data['temp_diff'] = data['Process temperature'] - data['Air temperature']

fig, ax = plt.subplots(1, 2, figsize = (10,4))

sns.histplot(data['Power'], bins = 20, ax = ax[0], color = 'red', alpha = 0.2, kde = True)
ax[0].set_ylabel("Frequency")

sns.boxplot(x = data['Power'], ax = ax[1], width = 0.25)
sns.rugplot(data, x = 'Power', hue = 'Machine failure', ax = ax[1], height = 0.1)
ax[1].set_xlabel("Count")

fig.suptitle("Distribution of Power(Watt)")

fig.show()

fig, ax = plt.subplots(1, 2, figsize = (10,4))

sns.histplot(data['temp_diff'], bins = 20, ax = ax[0], color = 'red', alpha = 0.2, kde = True)
ax[0].set_ylabel("Frequency")

sns.boxplot(x = data['temp_diff'], ax = ax[1], width = 0.25)
sns.rugplot(data, x = 'temp_diff', hue = 'Machine failure', ax = ax[1], height = 0.1)
ax[1].set_xlabel("Count")

fig.suptitle("Distribution of Temperature Difference")

fig.show()

"""##Data Preprocessing"""

# UDI and Product ID are high cardinality features, Removing Process Temperature due to multi-collinearity
data = data.drop(['UDI', 'Product ID', 'Air temperature', 'Process temperature', 'Rotational speed', 'Torque', 'Failure type'], axis = 1)

data = pd.get_dummies(data)

data[['Type_H', 'Type_L', 'Type_M']] = data[['Type_H', 'Type_L', 'Type_M']].astype('int')

data.head()

"""##Training Model"""

!pip -q install pycaret

!pip -q install --upgrade scipy

!pip install --upgrade pycaret

!pip -q install --upgrade yellowbrick

import pycaret

from pycaret.classification import *

s= setup(data, target = 'Machine failure', session_id = 42, data_split_stratify=True)

best_model = compare_models(sort = 'AUC')

save_model(best_model, 'predictive_maintenance')