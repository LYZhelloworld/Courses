#!/usr/bin/python
# Assignment 3

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

save_plot = True

def genSomeMixtureData(numData, probs, means, sigmadiags):
    # probs (1x3), i-th for p[i]
    # means (2x3)
    # sigmadiags (2x3), sigmadiags[k, i] for sigma[k]^2 of gaussian i
    # numdata: N
    # return: Nx2
    
    x = np.zeros((numData, 2))
    for n in range(numData):
        # Choose a feature space
        p = np.random.rand()
        if(p < probs[0][0]): # p1
            i = 0
        elif(p < probs[0][1]): # p2
            i = 1
        else: # p3
            i = 2
        
        while True:
            temp_result = np.random.normal(means[:, i], sigmadiags[:, i]) # Generate data
            if((temp_result > 0).all()):
                break # Waste
        x[n] = temp_result # Data that meet the criteria will be stored
        
    return x

################################################################
    
def kMeans(k, centres, data, error, return_cost = False):
    # centres (kx2)
    # data (Nx2)
    # error: epsilon
    m = centres[:]
    
    while(True):
        sets = [[] for i in range(k)]
        
        for point in data:
            # Calculate distance
            dist_sq = np.sum((point - m) ** 2, axis = 1)
            # Choose the nearest centre and add point into corresponding set
            sets[np.argmin(dist_sq)].append(point)
            
        temp_m = m[:]
        for i in range(len(sets)):
            if sets[i] != []:
                temp_m[i] = (np.mean(sets[i], axis = 0)) # centroid
            
        temp_m = np.array(temp_m)
        changes = temp_m - m
        m = temp_m
        
        if((changes < error).all()):
            break
    
    if(return_cost):
        costs = []
        for i in range(len(sets)):
            costs.append(np.average(np.sqrt(np.sum((m[i] - sets[i]) ** 2, axis = 1))))
        cost = np.average(costs)
        return m, cost
    else:
        return m
    
def kMeansChooseInitialCentres(k, data):
    # data (Nx2)
    # return: (kx2)
    min = np.amin(data, axis = 0)
    max = np.amax(data, axis = 0)
    return np.random.uniform(min, max, (k, 2))
    
def kMeansProblem(result):
    epsilon = 1e-4 # Error tolerance
    
    for k in [2, 3, 4, 8, 16]:
        centres = kMeans(k, kMeansChooseInitialCentres(k, result), result, epsilon)
        plt.plot(result[:, 0], result[:, 1], "b.", centres[:, 0], centres[:, 1], "r.")
        plt.axis("auto")
        plt.title("k-Means: k = " + str(k))
        if(save_plot):
            plt.savefig("k-means/k" + str(k) + ".png", dpi = 96)
        else:
            plt.show()
        plt.close()
        
################################################################

def kMeansPPChooseInitialCentres(k, data):
    # data (Nx2)
    # return: (kx2)
    x = kMeansChooseInitialCentres(1, data)
    
    while(len(x) < k):
        dists = []
        for centre in x:
            # Calculate distance
            dist_sq = np.sum((data - centre) ** 2, axis = 1)
            dists.append(dist_sq)
        prob = np.amin(dists, axis = 0)
        prob = prob / np.sum(prob)
        # Choose a new point
        #new_point = np.random.choice(data, 1, prob)
        new_point = data[np.random.choice(len(data), 1, p = prob)]
        x = np.concatenate((x, new_point), axis = 0)
    
    return x

def calculateD1(k, z):
    result = 0
    for j in range(k):
        for l in range(j - 1):
            result += np.sum((z[j] - z[l]) ** 2)
    result *= (2.0 / (k * (k - 1)))
    return result
    
def kMeansPPProblem(result):
    epsilon = 1e-4 # Error tolerance
    k_list = [2, 3, 4, 8, 16]
    avg1_list = []
    avg2_list = []
    
    for k in k_list:
        initial_centres = kMeansPPChooseInitialCentres(k, result)
        #avg1_list.append(calculateD1(k, initial_centres))
        centres = [kMeans(k, initial_centres, result, epsilon, return_cost = True) for i in range(10)]
        avg1_list.append(np.average([calculateD1(k, c[0]) for c in centres]))
        avg2_list.append(np.average([c[1] for c in centres]))
        
    plt.plot(k_list, avg1_list, "ro", k_list, avg2_list, "go")
    plt.axis("auto")
    plt.title("k-Means++")
    if(save_plot):
        plt.savefig("k-meansPP/result.png", dpi = 96)
    else:
        plt.show()
    plt.close()

################################################################
    
def kMedoidsData3D(data):
    # data (Nx2)
    max = np.amax(data, axis = 0)
    def calculate3D(point):
        return point[0] / (max[0] + 0.01), point[1] / (max[1] + 0.01), 1 - 0.5 * point[0] / (max[0] + 0.01) - 0.5 * point[1] / (max[1] + 0.01)
    # return: (Nx3)
    return np.array([list(calculate3D(point)) for point in data])

def kMedoidsChooseInitialCentres(k, data):
    # data (Nx3)
    # return: (kx3)
    return data[np.random.choice(len(data), k, replace=False)]

def kMedoids(k, centres, data, error, distance_func = None):
    # centres (kx3)
    # data (Nx3)
    # error: epsilon
    m = centres[:]
    
    if(distance_func is None):
        distance_func = lambda single_point, set: np.sum((single_point - set) ** 2, axis = 1)
    
    while(True):
        sets = [[] for i in range(k)]
        
        for point in data:
            # Calculate distance
            dist_sq = distance_func(point, m)
            # Choose the nearest centre and add point into corresponding set
            sets[np.argmin(dist_sq)].append(point)
            
        temp_m = m[:]
        for i in range(len(sets)):
            if sets[i] != []:
                # Find a suitable point for next centre
                distances = []
                for chosen_point in sets[i]:
                    distances.append(distance_func(chosen_point, sets[i]))
                temp_m[i] = sets[i][np.argmin(distances)]
            
        temp_m = np.array(temp_m)
        changes = temp_m - m
        m = temp_m
        
        if((changes < error).all()):
            break
    
    return m
    
def kMedoidsProblem(result, distance_func = None):
    epsilon = 1e-4 # Error tolerance
    k_list = [2, 3, 4, 8, 16]
    
    for k in k_list:
        initial_centres = kMedoidsChooseInitialCentres(k, result)
        centres = kMedoids(k, initial_centres, result, epsilon, distance_func)
        plt.plot(result[:, 0], result[:, 1], "b.", centres[:, 0], centres[:, 1], "r.")
        plt.axis("auto")
        if(distance_func is None):
            plt.title("k-Medoids: k = " + str(k))
        else:
            plt.title("k-Medoids (Chi-squared): k = " + str(k))
        if(save_plot):
            if(distance_func is None):
                plt.savefig("k-medoids/k" + str(k) + ".png", dpi = 96)
            else:
                plt.savefig("k-medoids-chi-squared/k" + str(k) + ".png", dpi = 96)
        else:
            plt.show()
        plt.close()

if __name__ == "__main__":   
    probs = np.array([[0.15, 0.3, 1 - 0.15 - 0.3]])
    means = np.array([[3, 3], [6, 3.6], [5.1, 9]]).T
    sigmadiags = np.array([[1, 1], [1, 0.5], [1, 1.5]]).T
    samples = 2000
    
    result = genSomeMixtureData(samples, probs, means, sigmadiags) # Generate data
    kMeansProblem(result)
    kMeansPPProblem(result)
    kMedoidsProblem(kMedoidsData3D(result))
    old_settings = np.seterr(all = "ignore")
    kMedoidsProblem(kMedoidsData3D(result),
        lambda single_point, set: np.sum((single_point - set) ** 2 / (single_point - set), axis = 1))
    np.seterr(**old_settings)