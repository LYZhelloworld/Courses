#!/usr/bin/python
# Assignment 2

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

DIM_SIZE = 48

def data_generator1(N):
    # variance (48 x N)
    variance = np.array([[1.0/(i + 1.0) for i in range(DIM_SIZE)] for x in range(N)]).T
    # error (1 x N)
    error = np.random.normal(0, 2, (1, N))
    # weight vector (48 x 1)
    v = np.ones((DIM_SIZE, 1))
    
    x = np.random.normal(0, np.sqrt(variance), (DIM_SIZE, N)) # x (48 x N)
    y = (v.T.dot(x) + error).T # y (N x 1)
    return x, y # (48 x N), (N x 1)
    
def gen_coefficients():
    # (48 x 1)
    return np.concatenate((np.random.uniform(0.6, 1, ((12, 1))), np.random.uniform(0, 0.2, ((36, 1)))))
    
def data_generator2(N, v):
    # v (48 x 1)
    # error (1 x N)
    error = np.random.normal(0, 2, (1, N))
    
    x = np.random.normal(0, np.ones((DIM_SIZE, N)), (DIM_SIZE, N)) # (48 x N)
    y = (v.T.dot(x) + error).T # y (N x 1)
    return x, y, v # (48 x N), (N x 1), (48 x 1)
    
def train_ridgeregression(x, y, l):
    # l: lambda
    # w = (XT * X + lambda * I) ^ -1 * XT * y
    # X (N x 48)
    # y (N x 1)
    # w (48 x 1)
    return np.linalg.inv(x.T.dot(x) + l).dot(x.T).dot(y)
    
def algorithm1(training, testing):
    x_train, y_train = data_generator1(training) # Generate training data
    x_test, y_test = data_generator1(testing) # Generate testing data
    l = 1e-30 # First lambda = 1*10^-30
    # x_train is 48 x N, so use transpose
    w = train_ridgeregression(x_train.T, y_train, l)
    # y^ = x * w
    # x (N x 48) (use transpose)
    # w (48 x 1)
    y_estimate = x_test.T.dot(w)
    # MSE = 1/n * sum((y^ - y) ^ 2)
    m1 = np.sum((y_estimate - y_test) ** 2) / testing
    
    # Similar code
    l = 5
    w = train_ridgeregression(x_train.T, y_train, l)
    y_estimate = x_test.T.dot(w)
    m2 = np.sum((y_estimate - y_test) ** 2) / testing
    
    return m1, m2
    
def algorithm2():
    x_sample, y_sample, v_sample = data_generator2(500, gen_coefficients()) # Generate samples
    # Result: (48 x N), (N x 1), (48 x 1)
    l = 1e-2 # lambda = 1*10^-2
    # Choose 400 for training and 100 for testing
    # Shuffle the array and choose top 400 for training and others for testing
    index = np.arange(500)
    np.random.shuffle(index)
    x_train = x_sample.T[index][:400] # Use transpose (N x 48)
    y_train = y_sample[index][:400]
    x_test = x_sample.T[index][400:] # Use transpose (N x 48)
    y_test = y_sample[index][400:]
    
    w = train_ridgeregression(x_train, y_train, l)
    y_estimate = x_test.dot(w)
    m1 = np.sum((y_estimate - y_test) ** 2) / 100
    
    return m1
    
def algorithm3():
    x_sample, y_sample, v_sample = data_generator2(500, gen_coefficients()) # Generate samples
    # Result: (48 x N), (N x 1), (48 x 1)
    l = 1e-2 # lambda = 1*10^-2
    # Use the similar shuffle algorithm as in algorithm2()
    index = np.arange(5)
    np.random.shuffle(index)
    # Build the shuffled data set
    data = []
    for i in range(5):
        data.append((x_sample.T[index[i] * 100 : (index[i] + 1) * 100],
                        y_sample[index[i] * 100 : (index[i] + 1) * 100]))
    
    e = [None] * 5
    for t in range(5):
        x_test = data[t][0]
        y_test = data[t][1]
        # Concatenate other data sets to get the training data
        data_train = data[:]
        del data_train[t]
        x_train = np.concatenate([i[0] for i in data_train])
        y_train = np.concatenate([i[1] for i in data_train])
        
        w = train_ridgeregression(x_train, y_train, l)
        y_estimate = x_test.dot(w)
        e[t] = np.sum((y_estimate - y_test) ** 2) / 100
    
    return np.average(e)
    
def ridge_regression():
    print "Ridge regression"
    print "Training samples = 100, Testing samples = 1000"
    m = np.array([list(algorithm1(100, 1000)) for i in range(10)])
    print "MSE of m1, m2:"
    print m
    
    print "Training samples = 500, Testing samples = 1000"
    m = np.array([list(algorithm1(500, 1000)) for i in range(10)])
    print "MSE of m1, m2:"
    print m
    
def cross_validation():
    print "Cross validation"
    print "Samples = 500, 400 for training, 100 for testing"
    m1 = np.array([algorithm2() for i in range(10)])
    print "MSE"
    print m1
    a1 = np.average(m1)
    v1 = np.var(m1)
    print "Avg =", a1, "Var =", v1
    print
    
    print "5-fold cross validation"
    m2 = np.array([algorithm3() for i in range(10)])
    print "MSE"
    print m2
    a2 = np.average(m2)
    v2 = np.var(m2)
    print "Avg =", a2, "Var =", v2
    
if __name__ == "__main__":
    ridge_regression()
    print "-------------------------"
    cross_validation()