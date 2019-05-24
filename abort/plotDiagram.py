import getSQLite
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

# TODO : Data dependent
start_year = getSQLite.start_year
end_year = getSQLite.end_year
total_year = end_year - start_year + 1
total_day = 365
field = "TEMP_AVG"


# Figure
fig = plt.figure()
ax = fig.gca(projection='3d')

# Get Data
# X : 365 days
# Y : year
# Z : value
X = np.arange(1, 365+1)
X = np.array([X, ] * total_year)
Y = np.arange(start_year, end_year+1)
Y = np.array([Y, ] * total_day)
Y = Y.transpose()

Z = np.array([getSQLite.getField(str(start_year), field)])
for year in range(start_year+1, end_year+1):
    temp_Z = np.array([getSQLite.getField(str(year), field)])
    Z = np.concatenate((Z, temp_Z), axis=0)

Z[Z==np.nan] = None

# Plot the surface
surf = ax.plot_surface(X, Y, Z,cmap=cm.coolwarm)



# Add a color bar which maps values to colors
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()