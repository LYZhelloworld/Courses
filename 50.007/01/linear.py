#!/usr/bin/python
# Linear Transformation
# Require: Python 2.7

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

save_plot = True # Debug = False

n = 100
x = np.random.normal([1, 3], 1, (n, 2)).T

# Plot: data points
print "Plotting data points..."
plt.plot(x[0, :], x[1, :], ".")
plt.axis([-6.0, 6.0, -6.0, 6.0])
plt.title("Data points")
if save_plot:
    plt.savefig("linear/data_points.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

# Mirror (y-axis)
a1 = np.array([[-1, 0], [0, 1]])
a1x = a1.dot(x)

# Plot: data points (y-axis)
print "Plotting data points (y-axis)..."
plt.plot(a1x[0, :], a1x[1, :], ".")
plt.axis([-6.0, 6.0, -6.0, 6.0])
plt.title("Data points (Mirror along y-axis)")
if save_plot:
    plt.savefig("linear/data_points_y.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

# Scale x-axis to 0.5
a2 = np.array([[0.5, 0], [0, 1]])
a2x = a2.dot(x)

# Plot: data points (scaled)
print "Plotting data points (scaled)..."
plt.plot(a2x[0, :], a2x[1, :], ".")
plt.axis([-6.0, 6.0, -6.0, 6.0])
plt.title("Data points (Scaled)")
if save_plot:
    plt.savefig("linear/data_points_scaled.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

# Rotate
a3 = np.array([[np.cos(np.pi / 4), np.sin(np.pi / 4)], [-np.sin(np.pi / 4), np.cos(np.pi / 4)]])
a3x = a3.dot(x)

# Plot: data points (rotated)
print "Plotting data points (rotated)..."
plt.plot(a3x[0, :], a3x[1, :], ".")
plt.axis([-6.0, 6.0, -6.0, 6.0])
plt.title("Data points (Rotated)")
if save_plot:
    plt.savefig("linear/data_points_rotated.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."

# Mirror (x-axis)
a4 = np.array([[1, 0], [0, -1]])

# Final
a5 = a2.dot(a1).dot(a4)
a5x = a5.dot(x)

# Plot: data points (final)
print "Plotting data points (final)..."
plt.plot(a5x[0, :], a5x[1, :], ".")
plt.axis([-6.0, 6.0, -6.0, 6.0])
plt.title("Data points (Final)")
if save_plot:
    plt.savefig("linear/data_points_final.png", dpi = 96)
else:
    plt.show()
plt.close()
print "Done."