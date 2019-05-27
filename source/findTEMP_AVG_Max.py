import getSQLite
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_year = getSQLite.start_year
end_year = getSQLite.end_year
total_day = 365


TEMP_AVG_max = []
TEMP_AVG_min = []
TEMP_MAX_max = []
TEMP_MAX_min = []
TEMP_MIN_max = []
TEMP_MIN_min = []
YEAR = np.arange(start_year, end_year+1)

# Find max occur in the year

for year in range(start_year, end_year+1):
    day = np.arange(1, total_day+1)
    data = getSQLite.getField(str(year), "TEMP_AVG")
    # If no value inside data
    if len(data[~pd.isna(data)]) == 0:
        TEMP_AVG_max.append(np.nan)
        TEMP_AVG_min.append(np.nan)
    else:
        index = pd.isna(data)
        day = day[~index]
        data = data[~index]

        TEMP_AVG_max.append(day[np.argmax(data)])
        TEMP_AVG_min.append(day[np.argmin(data)])

    day = np.arange(1, total_day + 1)
    data = getSQLite.getField(str(year), "TEMP_MAX")
    # If no value inside data
    if len(data[~pd.isna(data)]) == 0:
        TEMP_MAX_max.append(np.nan)
        TEMP_MAX_min.append(np.nan)
    else:
        index = pd.isna(data)
        day = day[~index]
        data = data[~index]

        TEMP_MAX_max.append(np.argmax(data) + 1)
        TEMP_MAX_min.append(np.argmin(data) + 1)

    day = np.arange(1, total_day + 1)
    data = getSQLite.getField(str(year), "TEMP_MIN")
    # If no value inside data
    if len(data[~pd.isna(data)]) == 0:
        TEMP_MIN_max.append(np.nan)
        TEMP_MIN_min.append(np.nan)
    else:
        index = pd.isna(data)
        day = day[~index]
        data = data[~index]

        TEMP_MIN_max.append(np.argmax(data) + 1)
        TEMP_MIN_min.append(np.argmin(data) + 1)

TEMP_AVG_max = np.asarray(TEMP_AVG_max)
TEMP_AVG_min = np.asarray(TEMP_AVG_min)
TEMP_MAX_max = np.asarray(TEMP_MAX_max)
TEMP_MAX_min = np.asarray(TEMP_MAX_min)
TEMP_MIN_max = np.asarray(TEMP_MIN_max)
TEMP_MIN_min = np.asarray(TEMP_MIN_min)

plt.figure(figsize=(8,6))
# avg_fig_max, = plt.plot(TEMP_AVG_max, YEAR, 'g.', label='AVG_max')
avg_fig_min, = plt.plot(TEMP_AVG_min, YEAR, 'g+', label='AVG_min')
# max_fig_max, = plt.plot(TEMP_MAX_max, YEAR, 'r.', label='MAX_max')
max_fig_min, = plt.plot(TEMP_MAX_min, YEAR, 'r+', label='MAX_min')
# min_fig_max, = plt.plot(TEMP_MIN_max, YEAR, 'b.', label='MIN_max')
min_fig_min, = plt.plot(TEMP_MIN_min, YEAR, 'b+', label='MIN_min')
plt.legend(loc='lower right')
plt.title("Temperature Max, Temperature Min", color='b')
plt.xlabel("DAY")
plt.ylabel("YEAR")
plt.xticks([16, 45, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350], \
           ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
plt.show()