#!/usr/bin/python
# K-nearest neighbors
# Require: Python 2.7

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

save_plot = True # Debug = False

# Generate training data
x2 = np.random.uniform(-1.0, 1.0, (5000, 2))

# Define a function for generating corresponding y
def generate_y(a):
    if np.random.rand(1)[0] > 0.25: # Probability that positive = 1 and negative = -1
        if a > 0:
            return 1
        else:
            return -1
    else:
        if a > 0:
            return -1
        else:
            return 1

v_generate_y = np.vectorize(generate_y)
# Generate labels of training data
y2 = v_generate_y(x2[:, 1])

# Generate testing data
x3 = np.random.uniform(-1.0, 1.0, (1000, 2))

# Plot of training data
print "Plotting training data..."
plt.plot(x2[y2 == 1][:, 0], x2[y2 == 1][:, 1], "r.", x2[y2 == -1][:, 0], x2[y2 == -1][:, 1], "b.")
plt.axis([-1.0, 1.0, -1.0, 1.0])
plt.title("Training data")
if save_plot:
    plt.savefig("k-nearest/training_data.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

def knn(xtrain, ytrain, xtest, k):
    def get_label(a, b):
        # Calculate euclidean distance, sort, and get the indices of top k results
        # No sqrt required
        sort_result = np.argsort((xtrain[:, 0] - a) ** 2 + (xtrain[:, 1] - b) ** 2)[:k]
        # Sign of the sum of these ytrain values is the result
        return (ytrain[sort_result].sum() > 0) * 2 - 1
    v_get_label = np.vectorize(get_label)
    return v_get_label(xtest[:, 0], xtest[:, 1])

y3 = knn(x2, y2, x3, 100)

# Plot of testing data
print "Plotting testing data..."
plt.plot(x3[y3 == 1][:, 0], x3[y3 == 1][:, 1], "r.", x3[y3 == -1][:, 0], x3[y3 == -1][:, 1], "b.")
plt.axis([-1.0, 1.0, -1.0, 1.0])
plt.title("Testing data")
if save_plot:
    plt.savefig("k-nearest/testing_data.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

def compute_error(train, test):
    # Not an error
    if train > 0 and test == 1:
        return 0
    elif train <= 0 and test == -1:
        return 0
    else: # Error
        return 1
v_compute_error = np.vectorize(compute_error)
error = v_compute_error(x3[:, 1], y3)

# Plot of 0-1 error
print "Plotting 0-1 error..."
plt.plot(error.T, "g.")
plt.axis([0, error.size, 0, 1.5])
plt.title("0-1 error")
if save_plot:
    plt.savefig("k-nearest/0-1_error.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

print "Average error rate = {0}".format(np.average(error))

x2a = x2 * [1000, 1]
x3a = x3 * [1000, 1]
y3a = knn(x2a, y2, x3a, 100)

# Plot of testing data (Scaled)
print "Plotting testing data (scaled)..."
plt.plot(x3a[y3a == 1][:, 0], x3a[y3a == 1][:, 1], "r.", x3a[y3a == -1][:, 0], x3a[y3a == -1][:, 1], "b.")
plt.axis([-1000.0, 1000.0, -1.0, 1.0])
plt.title("Testing data (Scaled)")
if save_plot:
    plt.savefig("k-nearest/testing_data_scaled.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

error_a = v_compute_error(x3a[:, 1], y3a)

# Plot of 0-1 error (Scaled)
print "Plotting 0-1 error (scaled)..."
plt.plot(error_a.T, "g.")
plt.axis([0, error_a.size, 0, 1.5])
plt.title("0-1 error (Scaled)")
if save_plot:
    plt.savefig("k-nearest/0-1_error_scaled.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

print "Average error rate (scaled) = {0}".format(np.average(error_a))

# Calculate standard deviation
std_x2 = np.std(x2, axis = 0)
print "Standard deviation = [{0}, {1}]".format(std_x2[0], std_x2[1])
std_x3 = np.std(x3, axis = 0)

x2b = x2 / std_x2
x3b = x3 / std_x3
y3b = knn(x2b, y2, x3b, 100)

# Plot of testing data (Divided by std)
print "Plotting testing data (divided by std)..."
plt.plot(x3b[y3b == 1][:, 0], x3b[y3b == 1][:, 1], "r.", x3b[y3b == -1][:, 0], x3b[y3b == -1][:, 1], "b.")
plt.axis([-2.0, 2.0, -1.0, 1.0])
plt.title("Testing data (Divided by STD)")
if save_plot:
    plt.savefig("k-nearest/testing_data_std.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

error_b = v_compute_error(x3b[:, 1], y3b)

# Plot of 0-1 error (Divided by std)
print "Plotting 0-1 error (divided by std)..."
plt.plot(error_b.T, "g.")
plt.axis([0, error_b.size, 0, 1.5])
plt.title("0-1 error (Divided by STD)")
if save_plot:
    plt.savefig("k-nearest/0-1_error_std.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

print "Average error rate (divided by std) = {0}".format(np.average(error_b))