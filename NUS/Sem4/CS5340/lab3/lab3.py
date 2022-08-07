""" CS5340 Lab 3: Hidden Markov Models
See accompanying PDF for instructions.
"""
import numpy as np
import scipy.stats
from scipy.special import softmax
from sklearn.cluster import KMeans
from scipy.stats import norm
import threading


class EmissionModel:
    def __init__(self, x, pi, A, phi):
        self.x = x
        self.pi = pi
        self.A = A
        self.phi = phi

        # constants
        self.N = len(x)
        self.K = len(pi)

        # cache
        self.alpha_cache = [None] * self.N
        self.beta_cache = [None] * self.N
        self.c_cache = [None] * self.N

        # generate alpha and beta
        # for seq_long, if alpha() and beta() are called directly, the maximum recursion depth is reached
        for i in range(self.N):
            self.alpha(i)
        for i in range(self.N):
            self.beta(self.N-i-1)

    def p_emission(self, n):
        return np.array([norm.pdf(self.x[n], self.phi['mu'][k], self.phi['sigma'][k]) for k in range(self.K)]) # 1 * K

    def alpha(self, n):
        if self.alpha_cache[n] is not None:
            return self.alpha_cache[n]
        if n == 0:
            self.alpha_cache[n] = self.pi * self.p_emission(n)
            self.c_cache[n] = np.sum(self.alpha_cache[n])
            self.alpha_cache[n] /= self.c_cache[n]
        else:
            self.alpha_cache[n] = self.alpha(n-1).dot(self.A) * self.p_emission(n)
            self.c_cache[n] = np.sum(self.alpha_cache[n])
            self.alpha_cache[n] /= self.c_cache[n]
        return self.alpha_cache[n] # 1 * K

    def beta(self, n):
        if self.beta_cache[n] is not None:
            return self.beta_cache[n]
        if n >= self.N - 1:
            self.beta_cache[n] = np.array([1] * self.K)
        else:
            self.beta_cache[n] = (self.beta(n+1) * self.p_emission(n+1)).dot(self.A.T)
            self.beta_cache[n] /= self.c_cache[n+1]
        return self.beta_cache[n] # 1 * K
        

class EmissionModelThread(threading.Thread):
    def __init__(self, x, pi, A, phi):
        super().__init__()
        self.x = x
        self.pi = pi
        self.A = A
        self.phi = phi

        self.gamma = None
        self.xi = None
    
    def run(self):
        model = EmissionModel(self.x, self.pi, self.A, self.phi)
        gamma = np.array([model.alpha(n) * model.beta(n) for n in range(model.N)])
        self.gamma = gamma

        xi = np.array([ \
            np.tile(model.alpha(n), (model.K, 1)).T * \
            np.tile(model.p_emission(n+1), (model.K, 1)) * \
            self.A * \
            np.tile(model.beta(n+1), (model.K, 1)) / model.c_cache[n+1] \
        for n in range(model.N-1)])
        self.xi = xi


class HmmModel:
    def __init__(self, pi, A, phi):
        self.pi = pi
        self.A = A
        self.phi = phi

    def __sub__(self, other):
        '''Calculate the changes of parameters.'''
        return np.max([np.max(np.absolute([
                self.pi - other.pi,
                self.phi['mu'] - other.phi['mu'],
                self.phi['sigma'] - other.phi['sigma']])),
            np.max(np.absolute(self.A - other.A))])


def initialize(n_states, x):
    """Initializes starting value for initial state distribution pi
    and state transition matrix A.

    A and pi are initialized with random starting values which satisfies the
    summation and non-negativity constraints.
    """
    seed = 5340
    np.random.seed(seed)

    pi = np.random.random(n_states)
    A = np.random.random([n_states, n_states])

    # We use softmax to satisify the summation constraints. Since the random
    # values are small and similar in magnitude, the resulting values are close
    # to a uniform distribution with small jitter
    pi = softmax(pi)
    A = softmax(A, axis=-1)

    # Gaussian Observation model parameters
    # We use k-means clustering to initalize the parameters.
    x_cat = np.concatenate(x, axis=0)
    kmeans = KMeans(n_clusters=n_states, random_state=seed).fit(x_cat[:, None])
    mu = kmeans.cluster_centers_[:, 0]
    std = np.array([np.std(x_cat[kmeans.labels_ == l]) for l in range(n_states)])
    phi = {'mu': mu, 'sigma': std}

    return pi, A, phi


"""E-step"""
def e_step(x_list, pi, A, phi):
    """ E-step: Compute posterior distribution of the latent variables,
    p(Z|X, theta_old). Specifically, we compute
      1) gamma(z_n): Marginal posterior distribution, and
      2) xi(z_n-1, z_n): Joint posterior distribution of two successive
         latent states

    Args:
        x_list (List[np.ndarray]): List of sequences of observed measurements
        pi (np.ndarray): Current estimated Initial state distribution (K,)
        A (np.ndarray): Current estimated Transition matrix (K, K)
        phi (Dict[np.ndarray]): Current estimated gaussian parameters

    Returns:
        gamma_list (List[np.ndarray]), xi_list (List[np.ndarray])
    """
    n_states = pi.shape[0]
    X = len(x_list)
    #gamma_list = [np.zeros([len(x), n_states]) for x in x_list]
    gamma_list = [None] * X
    #xi_list = [np.zeros([len(x)-1, n_states, n_states]) for x in x_list]
    #xi_list = []
    xi_list = [None] * X

    """ YOUR CODE HERE
    Use the forward-backward procedure on each input sequence to populate 
    "gamma_list" and "xi_list" with the correct values.
    Be sure to use the scaling factor for numerical stability.
    """
    # use multithreading due to the slow calculation
    thread_list = [EmissionModelThread(x, pi, A, phi) for x in x_list]
    for x in range(X):
        thread_list[x].start()

    for x in range(X):
        thread_list[x].join()
        gamma_list[x] = thread_list[x].gamma
        xi_list[x] = thread_list[x].xi

    return gamma_list, xi_list


"""M-step"""
def m_step(x_list, gamma_list, xi_list):
    """M-step of Baum-Welch: Maximises the log complete-data likelihood for
    Gaussian HMMs.
    
    Args:
        x_list (List[np.ndarray]): List of sequences of observed measurements
        gamma_list (List[np.ndarray]): Marginal posterior distribution
        xi_list (List[np.ndarray]): Joint posterior distribution of two
          successive latent states

    Returns:
        pi (np.ndarray): Initial state distribution
        A (np.ndarray): Transition matrix
        phi (Dict[np.ndarray]): Parameters for the Gaussian HMM model, contains
          two fields 'mu', 'sigma' for the mean and standard deviation
          respectively.
    """

    n_states = gamma_list[0].shape[1]
    pi = np.zeros([n_states])
    A = np.zeros([n_states, n_states])
    phi = {'mu': np.zeros(n_states),
           'sigma': np.zeros(n_states)}

    """ YOUR CODE HERE
    Compute the complete-data maximum likelihood estimates for pi, A, phi.
    """
    pi = np.sum([gamma[0] / np.sum(gamma[0]) for gamma in gamma_list], axis=0)
    pi /= np.sum(pi)

    N = gamma_list[0].shape[0]
    A = np.sum([np.sum([xi[n] for n in range(N-1)], axis=0) for xi in xi_list], axis=0)
    A /= np.sum(A, axis=1)[:, None]

    denominator = np.sum([np.sum(gamma_list[i], axis=0) for i in range(len(gamma_list))], axis=0)

    phi['mu'] = np.sum([np.sum(gamma_list[i] * np.tile(x_list[i][:, None], (1, n_states)), axis=0)
            for i in range(len(gamma_list))], axis=0)
    phi['mu'] /= denominator

    phi['sigma'] = np.sum([np.sum(gamma_list[i] * 
            np.power(np.tile(x_list[i][:, None], (1, n_states)) - np.tile(phi['mu'], (N, 1)), 2), axis=0)
            for i in range(len(gamma_list))], axis=0)
    phi['sigma'] /= denominator
    phi['sigma'] = np.sqrt(phi['sigma'])

    return pi, A, phi


"""Putting them together"""
def fit_hmm(x_list, n_states):
    """Fit HMM parameters to observed data using Baum-Welch algorithm

    Args:
        x_list (List[np.ndarray]): List of sequences of observed measurements
        n_states (int): Number of latent states to use for the estimation.

    Returns:
        pi (np.ndarray): Initial state distribution
        A (np.ndarray): Time-independent stochastic transition matrix
        phi (Dict[np.ndarray]): Parameters for the Gaussian HMM model, contains
          two fields 'mu', 'sigma' for the mean and standard deviation
          respectively.

    """

    # We randomly initialize pi and A, and use k-means to initialize phi
    # Please do NOT change the initialization function since that will affect
    # grading
    pi, A, phi = initialize(n_states, x_list)

    """ YOUR CODE HERE
     Populate the values of pi, A, phi with the correct values. 
    """
    threshold = 1e-4
    old = HmmModel(pi, A, phi)
    gamma_list, xi_list = e_step(x_list, pi, A, phi)
    pi, A, phi = m_step(x_list, gamma_list, xi_list)
    new = HmmModel(pi, A, phi)

    while new - old > threshold:
        #print(new-old)
        old = new
        gamma_list, xi_list = e_step(x_list, pi, A, phi)
        pi, A, phi = m_step(x_list, gamma_list, xi_list)
        new = HmmModel(pi, A, phi)

    return new.pi, new.A, new.phi
