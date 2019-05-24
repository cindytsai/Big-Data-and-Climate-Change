import getSQLite
import numpy as np

# TODO : Data dependent, FRSHTT Data
field = "TORNADO"
start_year = getSQLite.start_year
end_year = getSQLite.end_year
total_year = end_year - start_year + 1
total_day = 365

def findOne(array):
    '''
    find element which contains '1'
    :param array: np.array, shape(1, 365)
    :return format_array: np.array, shape(1, 365)
    '''

    format_array = []

    for i in range(len(array[0])):
        try:
            temp = ord(array[0][i])
            format_array.append(temp)
        except:
            format_array.append(np.nan)

    format_array = np.reshape(format_array, (1, len(format_array)))
    return format_array

# Get data
Z = np.array([getSQLite.getField(str(start_year), field)])
Z = findOne(Z)


for year in range(start_year+1, end_year+1):
    temp_Z = np.array([getSQLite.getField(str(year), field)])
    temp_Z = findOne(temp_Z)
    Z = np.concatenate((Z, temp_Z), axis=0)


Z_str = Z.astype(str)
Z_str[Z_str=='nan'] = ''
np.savetxt(field+".csv", Z, delimiter=",", fmt='%s')
