# -*- coding: utf-8 -*-
"""Solution_184181J.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TQ51yRwyyHM5n_9inyr-IYyJvz0cEuij

# **Assignment - Individual 184181J**
"""

from google.colab import drive
drive.mount('/content/drive')

"""## **Preprocessing**"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

""" Importing the dataset"""

df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/ML Asg/AirfoilSelfNoise.csv')
df

df.dtypes

"""Handling missing values"""

#Here the '0' values of columns other than 'alpha' (because 'alpha' means the angle of attack there for zero can be a value of an angle) are considered as missing values so they are converted to NaN
df[['f','c','U_infinity','delta']]=df[['f','c','U_infinity','delta']].replace(0, np.nan)
df = df.dropna() #drop all nan

df

#It seems that there are not null zero values in 'f','c','U_infinity','delta' columns and null values in all columns columns since all the 1503 rows are still here.

"""Handling Outliers

>  **Column 'f'**
"""

#Plotting the boxplot to observe outliers in column 'f'

import seaborn as sns

sns.boxplot(df['f'])

#There are 4 outliers

########### HANDLING OUTLIERS ######
Q1 = df.f.quantile(0.25)
Q3 = df.f.quantile(0.75)
print(Q1,Q3)
IQR = Q3-Q1
print(IQR)

lower_limit = Q1 - 1.5*IQR
upper_limit = Q3 + 1.5*IQR
print(lower_limit,upper_limit)

df = df
df['f'] = np.where(df['f']>upper_limit,upper_limit,df['f'])
df['f'] = np.where(df['f']<lower_limit,lower_limit,df['f'])

sns.boxplot(df['f'])

"""> **Column 'alpha'**"""

#Plotting the boxplot to observe outliers in column 'alpha'

import seaborn as sns

sns.boxplot(df['alpha'])

#There is 1 outlier

########### HANDLING OUTLIERS ######
Q1 = df.alpha.quantile(0.25)
Q3 = df.alpha.quantile(0.75)
print(Q1,Q3)
IQR = Q3-Q1
print(IQR)

lower_limit = Q1 - 1.5*IQR
upper_limit = Q3 + 1.5*IQR
print(lower_limit,upper_limit)

df = df
df['alpha'] = np.where(df['alpha']>upper_limit,upper_limit,df['alpha'])
df['alpha'] = np.where(df['alpha']<lower_limit,lower_limit,df['alpha'])

sns.boxplot(df['alpha'])

"""> **Column 'c'**"""

#Plotting the boxplot to observe outliers in column 'c'

import seaborn as sns

sns.boxplot(df['c'])  #There are no outliers

"""> **Column 'U_infinity'**"""

#Plotting the boxplot to observe outliers in column 'U_infinity'

import seaborn as sns

sns.boxplot(df['U_infinity']) #There are no outliers

"""> **Column 'delta'**"""

#Plotting the boxplot to observe outliers in column 'delta'

import seaborn as sns

sns.boxplot(df['delta'])

#There are 7 outliers

########### HANDLING OUTLIERS ######
Q1 = df.delta.quantile(0.25)
Q3 = df.delta.quantile(0.75)
print(Q1,Q3)
IQR = Q3-Q1
print(IQR)

lower_limit = Q1 - 1.5*IQR
upper_limit = Q3 + 1.5*IQR
print(lower_limit,upper_limit)

df = df
df['delta'] = np.where(df['delta']>upper_limit,upper_limit,df['delta'])
df['delta'] = np.where(df['delta']<lower_limit,lower_limit,df['delta'])

sns.boxplot(df['delta'])

"""Q-Q Plots and Histograms

> **Q-Q Plots**
"""

import scipy.stats as stats

stats.probplot(df["f"], dist="norm", plot=plt)
plt.show() #'f' is skewed

stats.probplot(df["alpha"], dist="norm", plot=plt)
plt.show() #'alpha' is skewed

stats.probplot(df["c"], dist="norm", plot=plt)
plt.show() #'c' is skewed

stats.probplot(df["U_infinity"], dist="norm", plot=plt)
plt.show() #'U_infinity' is skewed

stats.probplot(df["delta"], dist="norm", plot=plt)
plt.show() #'delta' is skewed

"""> **Histograms**"""

df['f'].hist() #'f' is right skewed

df['alpha'].hist() #'alpha' is right skewed

df['c'].hist() #'c' is right skewed

df['U_infinity'].hist() #'U_infinity' is not skewed

df['delta'].hist() #'delta' is right skewed

"""Transformations"""

from sklearn.preprocessing import FunctionTransformer

# create columns variables to hold the columns that need transformation
columns = ['f','alpha','c','delta']

#In column 'alpha' there are so many 0 values which shouldn't be dropped. So logarithm transformation cannot be used. There for inverse hyperbolic sine transformation is used

# create the function transformer object with logarithm transformation
arcsinh_transformer = FunctionTransformer(np.arcsinh, validate=True)

# apply the transformation to your data
data_new = arcsinh_transformer.transform(df[columns])
df_new = pd.DataFrame(data_new, columns=columns)

df_new

df[columns] = df_new #Update the dataset with transformed values

df #Updated dataset with transformed values

"""> Histograms after transformation"""

df['f'].hist()

df['alpha'].hist()

df['c'].hist()

df['delta'].hist()

"""> Since there are no any categorical features, encoding isn't apllied.

Standardization
"""

from sklearn.preprocessing import StandardScaler

# create the scaler object
scaler = StandardScaler()

data = pd.DataFrame(df, columns=['f', 'alpha','c', 'U_infinity', 'delta'])
# fit the scaler to the  data
scaler.fit(data)

train_scaled = scaler.transform(data)
df_scaled_columns = pd.DataFrame(train_scaled,columns=['f', 'alpha','c', 'U_infinity', 'delta'])
df_scaled_columns

df[['f', 'alpha','c','U_infinity', 'delta']] = df_scaled_columns #Update the dataset with transformed values

df

sns.displot(df[['f', 'alpha','c','U_infinity', 'delta']])

df[['f', 'alpha','c','U_infinity', 'delta']].hist()

"""> From these graphs we can see that the values in each feature are scaled into a general range.

## **Feature Engineering**

PCA
"""

from sklearn.decomposition import PCA

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

pca = PCA()
X_pca = pca.fit_transform(X) 
X_reduced = PCA(n_components=4).fit_transform(X) 

principalDf = pd.DataFrame(data = X_reduced)
principalDf.head(10)

X

X_reduced

X_pca

finalDf = pd.concat([principalDf, pd.DataFrame(y)], axis = 1)
finalDf.head(10)

#Feature 'delta' is removed after PCA

"""Correlation matrix"""

correlation_matrix = principalDf.corr()
correlation_matrix

correlation_matrix.shape

sns.heatmap(correlation_matrix, annot = True)
plt.show()

upper_tri = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape),k=1).astype(np.bool))
upper_tri

to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.99)]

to_drop #It can be seen that there are no correlated features. 'f', 'alpha', 'c', 'U_infinity' are independent features.

"""## **Training and Predicting**"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, Lasso, Ridge

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

trans = PolynomialFeatures(degree=4)
X_train = trans.fit_transform(X_train)
X_test = trans.transform(X_test)

#define cross-validation method to use
cv = KFold(n_splits=10, random_state=1, shuffle=True)

"""> Linear Regression with Cross Validation"""

model_lin = LinearRegression()
grid_lin = GridSearchCV(model_lin,{'fit_intercept':['True']}, cv=cv)
grid_lin.fit(X_train, y_train)
#use k-fold CV to evaluate model
scores_lin = cross_val_score(model_lin, X_train, y_train, scoring='neg_mean_squared_error',
                         cv=cv, n_jobs=-1)

#view mean absolute error
np.mean(np.absolute(scores_lin))

#Predict test set values
y_pred_lin = grid_lin.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred_lin.reshape(len(y_pred_lin),1), y_test.reshape(len(y_test),1)),1))

"""> Ridge Regression with Cross Validation"""

model_ridge = Ridge()
grid_ridge = GridSearchCV(model_ridge,{'alpha':['1']}, cv=cv)
grid_ridge.fit(X_train, y_train)
#use k-fold CV to evaluate model
scores_ridge = cross_val_score(model_ridge, X_train, y_train, scoring='neg_mean_squared_error',
                         cv=cv, n_jobs=-1)

#view mean absolute error
np.mean(np.absolute(scores_ridge))

#Predict test set values
y_pred_ridge = grid_ridge.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred_ridge.reshape(len(y_pred_ridge),1), y_test.reshape(len(y_test),1)),1))

"""> Lasso Regression with Cross Validation"""

model_lasso = Lasso()
grid_lasso = GridSearchCV(model_lasso,{'alpha': (np.logspace(-8, 8, 100))}, cv=cv)
grid_lasso.fit(X_train, y_train)

#use k-fold CV to evaluate model
scores_lasso = cross_val_score(model_lasso, X_train, y_train, scoring='neg_mean_squared_error',
                         cv=cv, n_jobs=-1)

#view mean absolute error
np.mean(np.absolute(scores_lasso))

#Predict test set values
y_pred_lasso = grid_lasso.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred_lasso.reshape(len(y_pred_lasso),1), y_test.reshape(len(y_test),1)),1))

"""## **Evaluation**"""

import math
from sklearn import metrics

"""> Linear Regression"""

print("Test(Loss): %f" % math.sqrt(metrics.mean_squared_error(y_test, y_pred_lin)))
print("Test(r-squared): %f" % metrics.r2_score(y_test, y_pred_lin))

"""> Ridge Regression"""

print("Test(Loss): %f" % math.sqrt(metrics.mean_squared_error(y_test, y_pred_ridge)))
print("Test(r-squared): %f" % metrics.r2_score(y_test, y_pred_ridge))

"""> Lasso Regression"""

print("Test(Loss): %f" % math.sqrt(metrics.mean_squared_error(y_test, y_pred_lasso)))
print("Test(r-squared): %f" % metrics.r2_score(y_test, y_pred_lasso))

#Plotting
Y_hat_lin = grid_lin.predict(X_test)
Y_hat_ridge = grid_ridge.predict(X_test)
Y_hat_lasso = grid_lasso.predict(X_test)
df_temp = pd.DataFrame()
df_temp['Y_hat_lin'] = Y_hat_lin
df_temp['Y_hat_ridge'] = Y_hat_ridge
df_temp['Y_hat_lasso'] = Y_hat_lasso
df_temp['Y'] = y_test
#df_temp['Label'] = Lable

pl_Y_lin = df_temp['Y_hat_lin']
pl_Y_ridge = df_temp['Y_hat_ridge']
pl_Y_lasso = df_temp['Y_hat_lasso']
pl_Y_true = df_temp['Y']
#pl_X_tick = df_temp['Label']

#fig, ax = plt.subplots()
plt.figure(figsize=(15, 8))
plt.plot(pl_Y_lin, label = "Linear Regression")
plt.plot(pl_Y_ridge, label = "Ridge Regression")
plt.plot(pl_Y_lasso, label = "Lasso Regression")
plt.plot(pl_Y_true, label = "Actual")
plt.legend()
#ax.set_xticklabels(pl_X_tick)