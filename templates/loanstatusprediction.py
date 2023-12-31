# -*- coding: utf-8 -*-
"""LoanStatusPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tcVL5C0N7QCMZvUDlL7WGX8CcCxKc2dq

Import Libraries
"""

import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle
import warnings

"""Reading the csv file"""

data=pd.read_csv("loandata.csv")
data.head()



"""Displaying the data information

"""

data.info()

"""Visualizing the data
#### Plotting the Loan Status i.e how much applicants are granted for loan
"""

def show_percent_bars(ax,feature):
  total=len(feature)
  for p in ax.patches:
        percentage = '{:.1f}%'.format(100 * p.get_height()/total)
        x = p.get_x() + p.get_width() / 2 - 0.05
        y = p.get_y() + p.get_height()
        ax.annotate(percentage, (x, y), size = 12)
        
ax = sns.countplot(data=data, x='Loan_Status')
ax.set_title("Loan Status", fontsize=20)
show_percent_bars(ax, data.Loan_Status)

plt.figure(figsize=(12,7))
sns.heatmap(data.corr(),annot=True)

plt.figure(figsize=(12,6))
sns.histplot(data=data, x='CoapplicantIncome', hue='Loan_Status', bins=30)
plt.xlabel("Coapplicant Income", fontsize=20)
plt.ylabel("Loan Status count",fontsize=20)

"""

Plotting Histogram between Application Income vs Loan Status"""

plt.figure(figsize=(12,6))
sns.histplot(data=data,x='ApplicantIncome', hue='Loan_Status', bins=30)
plt.xlabel("Applicant Income", fontsize=20)
plt.ylabel("Loan Status count",fontsize=20)

plt.figure(figsize=(12,6))
sns.histplot(data=data,x='LoanAmount', hue='Loan_Status', bins=30)
plt.xlabel("LoanAmount", fontsize=20)
plt.ylabel("Loan Status count",fontsize=20)

"""Plotting the subplots between independent and dependent variables"""

# making subplots
fig, axes = plt.subplots(2, 3, figsize=(20,8))

# set the spacing between subplots
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)

axes[0,0].set_title('Credit History', fontsize=20)
sns.countplot(ax=axes[0,0], data=data, x='Credit_History', hue='Loan_Status')

sns.countplot(ax=axes[0,1], data=data, x='Education', hue='Loan_Status')
axes[0,1].set_title("Education", fontsize=20)

sns.countplot(ax=axes[0,2], data=data, x='Gender',hue='Loan_Status')
axes[0,2].set_title("Gender", fontsize=20)



sns.countplot(ax=axes[1,0], data=data, x='Married',hue='Loan_Status')
axes[1,0].set_title("Married", fontsize=20)


sns.countplot(ax=axes[1,1], data=data, x='Property_Area', hue='Loan_Status')
axes[1,1].set_title("Property Area", fontsize=20)

sns.countplot(ax=axes[1,2], data=data, x='Dependents', hue='Loan_Status')
axes[1,2].set_title("Dependents", fontsize=20)

"""Data Prepocessing Steps

1.Checking for null values
"""

data.isnull().sum()

"""Seperating the numerical and categorial columns"""

data.drop('Loan_ID',axis=1,inplace=True)

data.isnull().sum()

data[data.Gender.isnull()]

data.Gender.value_counts()

mode_gender=data.Gender.mode()[0]
data.Gender.fillna(mode_gender,inplace=True)

print(data.loc[59])

data[data.Married.isnull()]

mode_married=data.Married.mode()[0]

data.Married.fillna(mode_married,inplace=True)

data.loc[41]

data[data.Dependents.isnull()]

data.Dependents.value_counts()

mode_Dependents=data.Dependents.mode()[0]

data.Dependents.fillna(mode_Dependents,inplace=True)

print(data.loc[11])

data[data.Self_Employed.isnull()]

mode_Self_Employed=data.Self_Employed.mode()[0]

data.Self_Employed.fillna(mode_Self_Employed,inplace=True)
print(data.loc[39])

data[data.LoanAmount.isnull()]

median_loanamount=data.LoanAmount.median()
print(median_loanamount)

data.LoanAmount.fillna(median_loanamount,inplace=True)
print(data.loc[104])

data[data.Loan_Amount_Term.isnull()]

median_Loan_Amount_Term=data.Loan_Amount_Term.mode()[0]

print(data.loc[3])

data.dropna(inplace=True)

data.reset_index(drop=True)

data[data.Credit_History.isnull()]

data.head()

data.columns

data.reset_index(drop=True,inplace=True)
data

cat_cols=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed','Credit_History', 'Property_Area']

for i in cat_cols:
    print(i)
    print('Train set:',sorted(data[i].unique()))

from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(handle_unknown = 'ignore')
load_df_encoded = ohe.fit_transform(data[cat_cols]).toarray()

load_df_encoded

len(load_df_encoded)

len(data)

loan_df=l=data.drop(cat_cols,axis=1);
print(loan_df.shape)

loan_df

loan_df=pd.concat([loan_df,pd.DataFrame(load_df_encoded, columns=ohe.get_feature_names_out(data[cat_cols].columns))],axis=1);
print(loan_df.shape)

loan_df.tail()

round(loan_df.Loan_Status.value_counts()/loan_df.shape[0]*100,2)

X=loan_df.drop('Loan_Status',axis=1)
Y=loan_df.Loan_Status

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 42)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

Y_train.value_counts()

from imblearn. over_sampling import SMOTE

X_train, Y_train=SMOTE (). fit_resample(X_train, Y_train)

Y_train.value_counts()

X_train.head()

model=RandomForestClassifier ()

model. fit(X_train, Y_train)

ypred=model.predict(X_test)
tr=model.score(X_train,Y_train)
te=model.score(X_test,Y_test)
print(f"Training Accuracy: {tr}\n\nTesting Accuracy: {te}\n")
Acc=accuracy_score(ypred,Y_test)
print("Accuracy: {:2f}%".format(Acc*100))
print("\nClassification Report :\n ",classification_report(Y_test,ypred))

with open('loanperdict.pkl','wb') as f:
   pickle.dump(model,f)

import json

columns={'data_columns':[col.lower() for col in X.columns]}
with open("columns.json","w") as f:
  f.write(json.dumps(columns))

X.columns