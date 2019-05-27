import getSQLite
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
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
ax = plt.axes(projection='3d')

# Get Data
# X : 365 days
# Y : year
# Z : value
X = np.arange(1, total_day+1)
X = np.array([X, ] * total_year)
Y = np.arange(start_year, end_year+1)
Y = np.array([Y, ] * total_day)
Y = Y.transpose()

df = pd.read_csv('../data/TEMP_AVG_Polyfit.csv', header=None)
Z = df.values

print(Z.shape)

# Plot the surface
surf = ax.plot_surface(X, Y, Z, rcount=total_year, ccount=total_day, cmap=cm.coolwarm)
fig.colorbar(surf, shrink=0.5, aspect=5)



plt.show()