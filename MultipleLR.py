####多员线性回归

from numpy import genfromtxt
import numpy as np
from sklearn import  datasets,linear_model


datapath ='deliveryDown.csv'
deliveryData = genfromtxt(datapath,delimiter=',')
print ('data')
print(deliveryData)

X = deliveryData[:,:-1]
Y = deliveryData[:,-1]
regr = linear_model.LinearRegression()
regr.fit(X,Y)
print('coefficient')
print(regr.coef_)
print('intercept')
print(regr.intercept_)

xPred = [102,0,1,0,6]
yPred = regr.predict(xPred)
print('yPred:',yPred)

