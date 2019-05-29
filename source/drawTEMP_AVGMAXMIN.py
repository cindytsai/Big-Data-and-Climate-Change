import getSQLite
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

every_day = 365


## Plot 2017
want_year = "2017"

day_max = np.arange(1, every_day+1)
day_min = np.arange(1, every_day+1)
day_avg = np.arange(1, every_day+1)

data_max = getSQLite.getField(want_year, "TEMP_MAX")
data_min = getSQLite.getField(want_year, "TEMP_MIN")
data_avg = getSQLite.getField(want_year, "TEMP_AVG")

# Cancel out None
nan_index = pd.isna(data_max)
day_max = day_max[~nan_index]
data_max = data_max[~nan_index]

nan_index = pd.isna(data_min)
day_min = day_min[~nan_index]
data_min = data_min[~nan_index]

nan_index = pd.isna(data_avg)
day_avg = day_avg[~nan_index]
data_avg = data_avg[~nan_index]

plt.figure(figsize=(3, 4))
fig_max, = plt.plot(day_max[0:31], data_max[0:31], 'r.-', label='Daily Maximum')
fig_min, = plt.plot(day_min[0:31], data_min[0:31], 'b.-', label='Daily Minimum')
fig_avg, = plt.plot(day_avg[0:31], data_avg[0:31], 'g.-', label='Daily Average')
plt.legend(loc='upper left')
plt.title("year = " + want_year, fontsize=16, color='b')
plt.xlabel("DAY")
plt.xticks([16], ('Jan'))
# plt.xticks([16, 45, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350], \
#            ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
plt.ylabel("Temperature($^\circ$C)")

plt.savefig(want_year + "TEMP_AVGMAXMIN" + '.png', bbox_inches="tight")
plt.close()