import getSQLite
import numpy as np

# TODO : Data dependent
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


def printData(field):
    '''
    print data initial
    TABLE YEAR
    FIELD TEMP_AVG
    :param field: string
    :return:
    '''

    Z = np.array([getSQLite.getField(str(start_year), field)])
    for year in range(start_year + 1, end_year + 1):
        temp_Z = np.array([getSQLite.getField(str(year), field)])
        Z = np.concatenate((Z, temp_Z), axis=0)

    Z_str = Z.astype(str)
    Z_str[Z_str == 'nan'] = ''
    np.savetxt(field + ".csv", Z, delimiter=",", fmt='%s')


def printDataMinor(field, table_name_minor, length):
    '''
    print manipulate data, with "minor" manipulation
    YEAR + field + _ + minor
    :param field:            string, data from initial data field EX: TEMP_AVG
    :param table_name_minor: string, data manipulation EX: FFT
    :param length:           int,    data length after manipulation
    :return:
    '''

    table_name = str(start_year) + field + "_" + table_name_minor

    # Set empty string
    nan_array = [np.nan] * length
    nan_array = np.asarray(nan_array)

    # Check if getTableIDMax == 0, some can't be manipulate, and stored nothing
    if getSQLite.getTableIDMax(table_name) == 0:
        Z = np.array([nan_array])

    else:
        Z = np.array([getSQLite.getField(table_name, table_name_minor)])

    for year in range(start_year+1, end_year+1):
        table_name = str(year) + field + "_" + table_name_minor

        # Get next Z, and check if ID max is 0 or not.
        if getSQLite.getTableIDMax(table_name) == 0:
            temp_Z = np.array([nan_array])
        else:
            temp_Z = np.array([getSQLite.getField(table_name, table_name_minor)])

        Z = np.concatenate((Z, temp_Z), axis=0)


    np.savetxt(field + "_" + table_name_minor + ".csv", Z, delimiter=",", fmt='%s')


def printDataColumn(table_name, column_name):
    '''
    print single Column data
    :param table_name: string
    :param column_name: string
    :return:
    '''
    Z = np.array(getSQLite.getField(table_name, column_name))
    np.savetxt(table_name+"_"+column_name+".csv", Z, delimiter=",", fmt='%s')