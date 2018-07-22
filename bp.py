#coding=utf-8
import numpy as np
def nonlin(x,deriv=False):
    if deriv ==  True:
        return x * (1-x)
    return 1 / (1 + np.exp(-x))

X = np.array([[0.35],[0.9]])
y = np.array([[0.5]])

np.random.seed(1)
W0 = np.array([[0.1,0.8],[0.4,0.6]])
W1 = np.array([[0.3,0.9]])
print('')

for j in range(100):
    l0 = X
    l1 = nonlin(np.dot(W0,l0))
    l2 = nonlin(np.dot(W1,l1))
    l2_error = y - l2
    Error = 1/2.0*(y-l2)**2
    l2_detal = l2_error * nonlin(l2,True)
    l1_error = l2_detal*W1
    l1_detal = l1_error * nonlin(l1,True)

    W1 += l2_detal*l1.T
    W0 += l0.T.dot(l1_detal)




