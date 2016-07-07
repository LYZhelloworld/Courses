import pdb
import numpy as np
import matplotlib.pyplot as plt
import math

######################################################################
#
# Learning algorithms and helpers
#
######################################################################

# Ordinary least squares regression
# X is an n x d matrix
# Y is an n x 1 matrix
# returns weights: d x 1 matrix
def ols(X, y):
    return (X.T * X).I * X.T * y

# "Ridge" regression with lambda = l; otherwise like ols
# Penalizes the offset weight, which is sometimes undesirable
def olsr(X, y, l = 0):
    d = X.shape[1]
    return (X.T * X + l * np.identity(d)).I * X.T * y

# Given an order for a polynomial feature space, d
# return a *function* that maps a single value into a vector of d+1 features
def polynomialFeatures(d):
    def p(xi):
        return np.matrix([xi[0,0]**i for i in range(d+1)])
    return p

# Given X, an array of training examples, and b, a bandwidth,
# return a *function* that maps a single value into a vector of features
def RBFs(X, b):
    # Your code here
    def p(xi):
        return np.matrix([np.array(np.linalg.norm(xi - x) / b) for x in X])
    return p

# Given a function, such as the one generated by polynomialFeatures,
# which takes a d-dimensional vector and returns a D-dimensional
# vector, and an n x d matrix X, return an n x D matrix of feature
# vectors
def applyFeatureFun(phi, X):
    return np.vstack([phi(X[i,:]) for i in range(X.shape[0])])

# Given a D x 1 weight vector and a "feature function" that takes a
# d-dimensional vector into a D x 1 vector, return a **function** that
# takes a d-dimensional vector into a scalar regression value, but
# mapping the input into the high-dimensional feature space and then
# taking the dot product with the weights.
def makeRegressor(w, phi):
    def r(x):
        return (phi(x)*w)[0,0]
    return r

# Given an n x d matrix X of input values and an n x 1 matrix y of
# target values, and a function that maps a row of X into a
# prediction, return the root mean squared error of the predictor
# applied to the X values.
def rmse(X, y, predictor):
    return np.sqrt(sse(X, y, predictor)/len(y))

# As for rmse, but just return the sum squared error.
def sse(X, y, predictor):
    p = np.matrix([predictor(X[i,:]) for i in range(X.shape[0])]).T
    assert p.shape == y.shape
    return np.sum(np.square(p - y))

######################################################################
#
# Data
#
######################################################################

# Uses data set from Chapter 1 of Bishop, stored in file
# "curvefitting.txt".  They are 10 points drawn from (x, sin(2 pi x))
# with noise added (but I'm not sure how much.)

# If random is not False, it should be an integer, and instead of
# returning data from the file, we will generate a new random data set
# of that size, with 0 mean, 0.2 stdev Gaussian noise.

# if addOnes is true, return: n x 1 matrix X, n x 2 matrix F (with
# column of 1's added) and n x 1 matrix Y.

def getCurveData(addOnes = False, random = False):
    if random:
        X = np.matrix([[i / float(random)] for i in range(random + 1)])
        noise = np.random.normal(scale = 0.2, size = (random+1, 1))
        y = np.matrix([[np.sin(2 * np.pi * X[i,0])] for i in range(X.shape[0])]) + noise
    else:
        data = np.loadtxt('curvefitting.txt')
        X, y = np.matrix(data[0]).T, np.matrix(data[1]).T
    if addOnes:
        F = np.append(np.ones_like(X), X, 1)
        return X, F, y
    else:
        return X, y

######################################################################
#
# Plotting stuff
#
######################################################################

def tidyPlot(xmin, xmax, ymin, ymax, center = False, title = None,
                 xlabel = None, ylabel = None):
    plt.ion()
    plt.figure(facecolor="white")
    ax = plt.subplot()
    if center:
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
    else:
        ax.spines["top"].set_visible(False)    
        ax.spines["right"].set_visible(False)    
        ax.get_xaxis().tick_bottom()  
        ax.get_yaxis().tick_left()
    eps = .05
    plt.xlim(xmin-eps, xmax+eps)
    plt.ylim(ymin-eps, ymax+eps)
    if title: ax.set_title(title)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    return ax

def plotData(ax, x, y, style = 'ro', label = None):
    if style is None:
        ax.plot(x, y, label = label)
    else:
        ax.plot(x, y, style, label = label)
    plt.show()

# w is a (1 x 2) matrix
def plotLine(ax, w, xmin, xmax, nPts = 100):
    b = float(w[0])
    m = float(w[1])
    plotFun(ax, lambda x: m*x + b, xmin, xmax, nPts)

def plotFun(ax, f, xmin, xmax, nPts = 100, label = None):
    x = np.linspace(xmin, xmax, nPts)
    y = np.vstack([f(np.matrix([[xi]])) for xi in x])
    ax.plot(x, y, label = label)
    plt.show()


def smooth(n, vals):
    # Run a box filter of size n
    x = sum(vals[0:n])
    result = [x]
    for i in range(n, len(vals)):
        x = x - vals[i-n] + vals[i]
        result.append(x)
    return result

######################################################################
#
# Tests
#
######################################################################

######################################################################
#
# Ordinary least squares in 2D (one constant input dimension)

def t1():
    X, F, y = getCurveData(True)

    w = ols(F, y)

    print 'w', w.T
    xmin, xmax = float(min(X)), float(max(X))
    ymin, ymax = float(min(y)), float(max(y))
    ax = tidyPlot(xmin, xmax, ymin, ymax, xlabel = 'x', ylabel = 'y')
    plotData(ax, X, y)
    plotLine(ax, w, xmin, xmax)

######################################################################
#
# Ordinary least squares in polynomial feature spaces
# Plots predictors

def t2(ds = range(1, 10)):
    X, y = getCurveData()
    xmin, xmax = float(min(X)), float(max(X))
    ymin, ymax = float(min(y)), float(max(y))
    ax = tidyPlot(xmin, xmax, ymin-1, ymax+1, xlabel = 'x', ylabel = 'y')

    plotData(ax, X, y)

    for d in ds:
        phi = polynomialFeatures(d)
        phiD = applyFeatureFun(phi, X)
        w = ols(phiD, y)
        predictor = makeRegressor(w, phi)

        plotFun(ax, predictor, xmin, xmax, label = str(d))
        print 'Order', d, 'Training RMSE', rmse(X, y, predictor)
        print '     w', w.T
    ax.legend(loc="upper left", bbox_to_anchor=(1,1))

######################################################################
#
# Ordinary least squares in polynomial feature spaces
# Plots train and test error versus order of polynomial basis

def t3(ds = range(1, 10)):
    X, y = getCurveData()
    XTest, yTest = getCurveData(random = 10)
    xmin, xmax = float(min(X)), float(max(X))
    ymin, ymax = float(min(y)), float(max(y))
    ax = tidyPlot(xmin, xmax, ymin-1, ymax+1, xlabel = 'x', ylabel = 'y')
    plotData(ax, X, y)
    plotData(ax, XTest, yTest, style = 'go')
    trainErr = []
    testErr = []

    for d in ds:
        phi = polynomialFeatures(d)
        phiD = applyFeatureFun(phi, X)
        w = ols(phiD, y)
        predictor = makeRegressor(w, phi)
        plotFun(ax, predictor, xmin, xmax)
        trainErr.append(rmse(X, y, predictor))
        testErr.append(rmse(XTest, yTest, predictor))
        print 'Order', d, 'Training RMSE', trainErr[-1]
        print '        Test RMSE', testErr[-1]

    ax = tidyPlot(0, len(ds), 0, max(max(testErr), max(trainErr)), center =True,
                      xlabel = 'Polynomial order', ylabel = 'RMSE')
    ax.plot(ds, trainErr, label = 'test err')
    ax.plot(ds, testErr, label = 'train err')
    ax.legend()

######################################################################
#
# Ordinary least squares in RBF feature spaces
# Plots train and test error versus bandwidth

# LPK: these are good b values (.01, .05, .1, .5, 1, 2, 4)

def tRBF(bs = [.01, .05, .1, .5, 1.0, 2.0, 4.0]):
    X, y = getCurveData()
    XTest, yTest = getCurveData(random = 10)
    xmin, xmax = float(min(X)), float(max(X))
    ymin, ymax = float(min(y)), float(max(y))
    ax = tidyPlot(xmin, xmax, ymin-1, ymax+1, xlabel = 'x', ylabel = 'y')
    plotData(ax, X, y)
    trainErr = []
    testErr = []

    for b in bs:
        phi = RBFs(X, b)
        phiD = applyFeatureFun(phi, X)
        w = olsr(phiD, y, 1e-5) 
        predictor = makeRegressor(w, phi)
        plotFun(ax, predictor, xmin, xmax, label = str(b))
        trainErr.append(rmse(X, y, predictor))
        testErr.append(rmse(XTest, yTest, predictor))
        print 'Bandwidth', b, 'Training RMSE', trainErr[-1]
        print '        Test RMSE', testErr[-1]
        print '    w', w.T
    ax.legend(loc = 'best')

    if len(bs) > 1:
        ax = tidyPlot(min(bs), max(bs), 0, max(max(testErr), max(trainErr)),
                        xlabel = 'Bandwidth', ylabel = 'RMSE')
        ax.plot(bs, trainErr, label = 'test err')
        ax.plot(bs, testErr, label = 'train err')
        ax.legend(loc = 'best')


######################################################################
#
# Ordinary least squares in polynomial feature spaces
# Plots train and test error versus size of training set

def t4(trainSizes = (10, 15, 20, 30, 50, 100), showData = False):
    XTest, yTest = getCurveData(random = 100)
    xmin, xmax = float(np.min(XTest)), float(np.max(XTest))
    ymin, ymax = float(np.min(yTest)), float(np.max(yTest))
    trainErr = []
    testErr = []
    phi = polynomialFeatures(9)

    if not showData:
        ax = tidyPlot(xmin, xmax, ymin-1, ymax+1, xlabel = 'x', ylabel = 'y',
                          title = 'Predictors for different train sizes')

    for ts in trainSizes:
        X, y = getCurveData(random = ts-1)
        if showData:
            ax = tidyPlot(xmin, xmax, ymin-1, ymax+1, xlabel = 'x', ylabel = 'y',
                          title = 'Train size = ' + str(ts))
            plotData(ax, X, y)
        phiD = applyFeatureFun(phi, X)
        w = ols(phiD, y)
        predictor = makeRegressor(w, phi)
        plotFun(ax, predictor, xmin, xmax, label=str(ts))
        trainErr.append(rmse(X, y, predictor))
        testErr.append(rmse(XTest, yTest, predictor))
        print 'Train size', ts, 'Training RMSE', trainErr[-1]
        print '        Test RMSE', testErr[-1]
        print '     w', w.T
    ax.legend(loc="upper left", bbox_to_anchor=(1,1))
    if len(trainSizes) > 1:
        ax = tidyPlot(0, max(trainSizes), 0, max(testErr), center = True,
                      xlabel = 'Training set size', ylabel = 'RMSE')
        ax.plot(trainSizes, trainErr, label = 'test err')
        ax.plot(trainSizes, testErr, label = 'train err')
        ax.legend(loc="upper right")


######################################################################
#
# Ridge regression in polynomial feature spaces
# Plot train and test error versus ridge parameter lambda

def t5(logLambdaValues = (-50, -40, -30, -20, -15, -10, -1, 0, 1, 10)):
    XTest, yTest = getCurveData(random = 100)
    xmin, xmax = float(np.min(XTest)), float(np.max(XTest))
    ymin, ymax = float(np.min(yTest)), float(np.max(yTest))
    trainErr = []
    testErr = []
    phi = polynomialFeatures(9)

    ax = tidyPlot(xmin, xmax, ymin-1, ymax+1,
                      xlabel = 'x', ylabel = 'y',
                          title = 'Predictors for different lambda values')
    X, y = getCurveData()
    phiD = applyFeatureFun(phi, X)
    plotData(ax, X, y)
    for llv in logLambdaValues:
        w = olsr(phiD, y, np.exp(llv))
        predictor = makeRegressor(w, phi)
        plotFun(ax, predictor, xmin, xmax, label=str(llv))
        trainErr.append(rmse(X, y, predictor))
        testErr.append(rmse(XTest, yTest, predictor))
        print 'Log lambda', llv, 'Training RMSE', trainErr[-1]
        print '        Test RMSE', testErr[-1]
        print w.T
    ax.legend(loc="upper left", bbox_to_anchor=(1,1))

    if len(logLambdaValues) > 1:
        ax = tidyPlot(min(logLambdaValues), max(logLambdaValues),
                        0, max(testErr), center = True,
                        xlabel = 'Log lambda', ylabel = 'RMSE')
        ax.plot(logLambdaValues, trainErr, label = 'train err')
        ax.plot(logLambdaValues, testErr, label = 'test err')
        ax.legend(loc="best")
    

print 'Loaded learn.py'
