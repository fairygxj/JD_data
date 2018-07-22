import numpy as np
import random

def getData(numspoints,bias,variance):
    x = np.zeros(shape=(numspoints,2))
    y = np.zeros(shape= numspoints)
    for  i in range(0,numspoints):
        x[i][0] = 1
        x[i][1] = i
        y[i] = (i + bias) + random.uniform(0,1) * variance
    return x,y



def gradientDenscent(x,y,theta,alpha,m,numIteration):
    xTrans = x.transpose()
    for i in range(0,numIteration):
        hypothesis = np.dot(x,theta)
        loss = hypothesis - y
        cost = np.sum(loss **2)/(2 * m)
        print('iteration',i,'cost',cost)
        gradient = np.dot(xTrans,loss) / m
        theta = theta - alpha * gradient
    print('*****************',theta)
    return theta



x,y = getData(100,25,10)
m,n = np.shape(x)
theta = np.ones(n)
alpha = 0.0005
numIteration = 100000
gradientDenscent(x,y,theta,alpha,m,numIteration)
