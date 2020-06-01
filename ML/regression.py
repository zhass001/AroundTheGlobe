import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

def analysis(): # Not required for final evaluation
    onlyLinear = True
    df = pd.read_csv('training_data.csv')
    X = df[['Views', 'Favorites', 'Comments']]
    Y = df[['Score']]

    for i in range(len(X.columns)):
        sns.lmplot(x =X.columns[i], y =Y.columns[0], data = df, order = 1, ci = None)

    loocv = LeaveOneOut()
    error = []
    Predictions = []
    Targets = []
    for train_index, test_index in loocv.split(df):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = Y.iloc[train_index], Y.iloc[test_index]

        if not onlyLinear:
            polynomial_features= PolynomialFeatures(degree=2)
            X_train = polynomial_features.fit_transform(X_train)
            X_test = polynomial_features.fit_transform(X_test)

        regr = LinearRegression()
        regr.fit(X_train, y_train)
        predictions = regr.predict(X_test)
        Predictions.append(predictions.squeeze())
        targets = y_test.values
        Targets.append(targets.squeeze())
        error.append(np.abs(predictions-targets))


    rmse = np.sqrt(np.mean( np.array(error)**2))
    r2 = r2_score(np.array(Targets), np.array(Predictions))
    print("Root Mean Square Error: "+ str(rmse))
    #print(r2)

def train_whole():
    # Whole Model
    df = pd.read_csv('training_data.csv')
    X = df[['Views', 'Favorites', 'Comments']]
    Y = df[['Score']]

    regr = LinearRegression()
    regr.fit(X, Y)
    return regr

def predict(X, regr):
    if len(np.shape(X))==1:
        X = np.array(X)
        X = X.reshape(1,-1)
    return regr.predict(X).squeeze()

if __name__ == "__main__":
    analysis() # Not required in final evaluation. Only for analysis
    model = train_whole()
    coef = model.coef_
    intercept = model.intercept_
    print("Intercept value : " + str(intercept))
    print("Coef of Views : "+ str(coef[0][0]))
    print("Coef of Favorites : "+ str(coef[0][1]))
    print("Coef of Comments : "+ str(coef[0][2]))
    output = predict([123297, 393, 19], model)
    print("Predicted Score of input [123297, 393, 19] is: "+str(output))
