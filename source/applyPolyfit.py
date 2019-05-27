import getSQLite
import numpy as np
import pandas as pd

# TODO: field dependent
want_field = "TEMP_MIN"
table_name_minor = "Polyfit"

start_year = getSQLite.start_year
end_year = getSQLite.end_year

def applyPolyfit(x, y, deg):
    '''
    delete np.nan data, then np.polyfit deg
    :param x: np.array; x may contain np.nan, we will remove this later.
    :param y: np.array; y may contain np.nan, we will remove this later.
    :param deg: int; degree of polynomial
    :return y_fit: np.array; y_fit polynomial value of len(x)
    '''

    # Canceled out np.nan in y index, and related x index
    nan_index = pd.isna(y)
    x_fit = x[~nan_index]
    y_fit = y[~nan_index]
    # Canceled out np.nan in x index, and related y index
    nan_index = pd.isna(x_fit)
    x_fit = x_fit[~nan_index]
    y_fit = y_fit[~nan_index]
    # np.polyfit deg=4
    y_fit_value = []

    try:
        y_fit_result = np.polyfit(x_fit, y_fit, deg)

        for i in range(len(x)):
            y_fit_value.append(np.polyval(y_fit_result, x[i]))
        y_fit_value = np.asarray(y_fit_value)

    except:
        y_fit_value = []

    return y_fit_value


for year in range(start_year, end_year+1):
    # Check ID, if == 0 then continue
    if getSQLite.getTableIDMax(str(year)) == 0:
        getSQLite.createTable(str(year) + want_field + "_" + table_name_minor)
        print(year)
        continue

    # Get data
    y = getSQLite.getField(str(year), want_field)
    x = np.arange(1, 366)
    y_fit = applyPolyfit(x, y, 4)

    # Load into database
    table_name = str(year) + want_field + "_" + table_name_minor
    getSQLite.createTable(table_name)
    getSQLite.createTableColumn(table_name, table_name_minor, "REAL")
    getSQLite.insertField(table_name, table_name_minor, y_fit)
    print(year)
