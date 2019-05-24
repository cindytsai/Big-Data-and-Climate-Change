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
X = np.arange(1, 4)
X = np.array([X, ] * 3)
Y = np.arange(2, 5)
Y = np.array([Y, ] * 3)
Y = Y.transpose()

# Can't draw np.nan
# C:\Python36\lib\site-packages\numpy\core\_methods.py:29: RuntimeWarning: invalid value encountered in reduce
#   return umr_minimum(a, axis, None, out, keepdims)
# C:\Python36\lib\site-packages\numpy\core\_methods.py:26: RuntimeWarning: invalid value encountered in reduce
#   return umr_maximum(a, axis, None, out, keepdims)
# C:\Python36\lib\site-packages\matplotlib\colors.py:489: RuntimeWarning: invalid value encountered in less
#   np.copyto(xa, -1, where=xa < 0.0)

Z = np.array([[3,5,3],
              [4,6,7],
              [1,2,np.nan]])



# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

# Add a color bar which maps values to colors
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()