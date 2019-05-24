import getSQLite
import numpy as np

# TODO : Data dependent
field = "WDSP_MAX"
start_year = getSQLite.start_year
end_year = getSQLite.end_year
total_year = end_year - start_year + 1
total_day = 365


# Get Data
# X : 365 days
# Y : year
# Z : value
# X = np.arange(1, total_day+1)
# X = np.array([X, ] * total_year)
# Y = np.arange(start_year, end_year+1)
# Y = np.array([Y, ] * total_day)
# Y = Y.transpose()


Z = np.array([getSQLite.getField(str(start_year), field)])
for year in range(start_year+1, end_year+1):
    temp_Z = np.array([getSQLite.getField(str(year), field)])
    Z = np.concatenate((Z, temp_Z), axis=0)

# np.savetxt("X_Day.csv", X, delimiter=",", fmt='%d')
# np.savetxt("Y_Year.csv", Y, delimiter=",", fmt='%d')

Z_str = Z.astype(str)
Z_str[Z_str=='nan'] = ''
np.savetxt(field+".csv", Z, delimiter=",", fmt='%s')
