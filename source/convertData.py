import sqlite3
import numpy as np

# FOR Global Summary of the Day GSOD file
# station dependent
# WBAN_GSOD.db
station_STN = "722860"
station_WBAN = "23119"
start_year = 1933
end_year = 2018
ID_max = 29541

# SQLite
conn = sqlite3.connect(station_WBAN+'_GSOD.db')
cursor = conn.cursor()

'''
@:param table_name string
'''
def createTABLE(table_name) :
    sql_cmd = "CREATE TABLE IF NOT EXISTS " + "`" +table_name + "`"\
              "(ID       INTEGER PRIMARY KEY AUTOINCREMENT," \
              "STN       TEXT, WBAN TEXT, YEARMODA TEXT," \
              "TEMP_AVG	 REAL, TEMP_COUNT    INTEGER," \
              "DEWP_AVG	 REAL, DEWP_COUNT    INTEGER," \
              "SLP_AVG   REAL, SLP_COUNT	 INTEGER," \
              "STP_AVG	 REAL, STP_COUNT	 INTEGER," \
              "VISIB_AVG REAL, VISIB_COUNT	 INTEGER," \
              "WDSP_AVG	 REAL, WDSP_COUNT	 INTEGER," \
              "MXSPD	 REAL, " \
              "WDSP_MAX	 REAL, " \
              "TEMP_MAX	 REAL," \
              "TEMP_MIN	 REAL," \
              "PRCP	     REAL, PRCP_FLAG	 TEXT," \
              "SNDP	     REAL," \
              "FOG	     INTEGER," \
              "RAIN	     INTEGER," \
              "SNOW	     INTEGER," \
              "HAIL      INTEGER," \
              "THUNDER   INTEGER," \
              "TORNADO   INTEGER)"
    cursor.execute(sql_cmd)

'''
@:param table_name string
@:param values     list
'''
def insertVALUES(table_name, values) :
    sql_cmd = "INSERT INTO " + "`" + table_name + "`" \
              " (STN, WBAN, YEARMODA, TEMP_AVG, TEMP_COUNT, DEWP_AVG, DEWP_COUNT, SLP_AVG, SLP_COUNT," \
              "  STP_AVG, STP_COUNT, VISIB_AVG, VISIB_COUNT, WDSP_AVG, WDSP_COUNT," \
              "  MXSPD, WDSP_MAX, TEMP_MAX, TEMP_MIN, PRCP, PRCP_FLAG, SNDP," \
              "  FOG, RAIN, SNOW, HAIL, THUNDER, TORNADO) VALUES " \
              "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(sql_cmd, (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                             values[8], values[9], values[10],values[11],values[12],values[13],values[14],values[15],
                             values[16],values[17],values[18],values[19],values[20],values[21],values[22],values[23],
                             values[24],values[25],values[26],values[27]))
    conn.commit()


'''
@:param table_name string
@:param field      string
@:param nan_value  according to value's data type
@:return array     np.array
'''
def readFIELD(table_name, field, nan_value) :
    sql_cmd = "SELECT "+ field +" FROM " + "`" + table_name + "`"
    cursor.execute(sql_cmd)

    # Change to np.array type
    array = []
    for value in cursor.fetchall() :
        array.append(value[0])
    array = np.asarray(array)

    # Let missing value as np.nan
    array[array==nan_value] = np.nan

    return array

'''
@:param table_name string
@:param field      string
@:param where      string
@:param nan_value  according to data type
@:return value     according to data type
'''
def readFIELDWHERE(table_name, field, where, nan_value) :
    sql_cmd = "SELECT " + field + " FROM " + "`" + table_name + "`" + " WHERE " + where
    cursor.execute(sql_cmd)
    value = np.nan
    for row in cursor.fetchall() :
        value = row[0]
        if value == nan_value:
            value = np.nan
    return value


# for year in range(start_year, end_year+1):
#     cursor.execute("DROP TABLE " + "`" + str(year) + "`")

# CREATE year TABLES
# for year in range(start_year, end_year+1):
#     print (year)
#     createTABLE(str(year))


# Read from table WBAN_GSOD_RAW.db
# Convert units TEMP_AVG, DEWP_AVG, TEMP_MAX, TEMP_MIN
# Fahrenheit -> Cecilius
nan_value = 9999.9
# Convert units TEMP_AVG, DEWP_AVG (without FLAGS)
array_TEMP_AVG = readFIELD(station_WBAN+"_GSOD_RAW", "TEMP_AVG", nan_value)
array_TEMP_AVG = np.around((5./9.) * (array_TEMP_AVG - 32), decimals=3)
array_DEWP_AVG = readFIELD(station_WBAN+"_GSOD_RAW", "DEWP_AVG", nan_value)
array_DEWP_AVG = np.around((5./9.) * (array_DEWP_AVG - 32), decimals=3)
# Convert units TEMP_MAX, TEMP_MIN (with FLAGS)
array_TEMP_MAX = []
array_TEMP_MIN = []
for i in range(1, ID_max+1) :
    temp_string = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "TEMP_MAX", "ID = " + str(i), nan_value)
    if temp_string == str(nan_value):
        array_TEMP_MAX.append(np.nan)
        continue
    # Check if it has a flag *
    if temp_string[-1] == "*":
        temp_string = temp_string[:-1]
    temp = float(temp_string)
    array_TEMP_MAX.append(temp)
array_TEMP_MAX = np.asarray(array_TEMP_MAX)
array_TEMP_MAX = np.around((5./9.) * (array_TEMP_MAX - 32), decimals=3)

for i in range(1, ID_max+1) :
    temp_string = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "TEMP_MIN", "ID = " + str(i), nan_value)
    if temp_string == str(nan_value):
        array_TEMP_MIN.append(np.nan)
        continue
    # Check if it has a flag *
    if temp_string[-1] == "*":
        temp_string = temp_string[:-1]
    temp = float(temp_string)
    array_TEMP_MIN.append(temp)
array_TEMP_MIN = np.asarray(array_TEMP_MIN)
array_TEMP_MIN = np.around((5./9.) * (array_TEMP_MIN - 32), decimals=3)

# Convert units SLP_AVG, STP_AVG
# millibar = 0.001 bar = 0.000986923 atm
nan_value = 9999.9
array_SLP_AVG = readFIELD(station_WBAN+"_GSOD_RAW", "SLP_AVG", nan_value)
array_SLP_AVG = np.around(0.000986923 * array_SLP_AVG, decimals=3)
array_STP_AVG = readFIELD(station_WBAN+"_GSOD_RAW", "STP_AVG", nan_value)
array_STP_AVG = np.around(0.000986923 * array_STP_AVG, decimals=3)

# Convert units VISIB_AVG
# mile = 1609.34 m = 1.60934 km
nan_value = 999.9
array_VISIB_AVG = readFIELD(station_WBAN+"_GSOD_RAW", "VISIB_AVG", nan_value)
array_VISIB_AVG = np.around(1.60934 * array_VISIB_AVG, decimals=3)

# Convert units WDSP_AVG, MXSPD, WDSP_MAX
# knot = 0.514444 m/s
nan_value = 999.9
array_WDSP_AVG = readFIELD(station_WBAN+"_GSOD_RAW", "WDSP_AVG", nan_value)
array_WDSP_AVG = np.around(0.514444 * array_WDSP_AVG, decimals=3)
array_MXSPD = readFIELD(station_WBAN+"_GSOD_RAW", "MXSPD", nan_value)
array_MXSPD = np.around(0.514444 * array_MXSPD, decimals=3)
array_WDSP_MAX = readFIELD(station_WBAN+"_GSOD_RAW", "WDSP_MAX", nan_value)
array_WDSP_MAX = np.around(0.514444 * array_WDSP_MAX)

# Convert units PRCP, PRCP_FLAG
# np.nan means 0 here
# inch = 2.54 cm
nan_value = 99.99
array_PRCP = []
PRCP_FLAG = []
for i in range(1, ID_max+1):
    temp_string = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "PRCP", "ID = " + str(i), nan_value)
    if temp_string == str(nan_value):
        array_PRCP.append(np.nan)
        PRCP_FLAG.append(np.nan)
        continue
    # Check if it has a flag
    prcp_flag = 0
    for char in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
        if temp_string[-1] == char:
            prcp_flag = char
            break
    # If no flag
    if prcp_flag == 0:
        array_PRCP.append(float(temp_string))
        PRCP_FLAG.append(np.nan)
    if type(prcp_flag) == str:
        array_PRCP.append(float(temp_string[:-1]))
        PRCP_FLAG.append(prcp_flag)
array_PRCP = np.asarray(array_PRCP)
array_PRCP = np.around(2.54 * array_PRCP, decimals=3)
array_PRCP[np.isnan(array_PRCP)] = 0

# Convert unit SNDP
# np.nan here means 0
# inch = 2.54 cm
nan_value = 999.9
array_SNDP = readFIELD(station_WBAN+"_GSOD_RAW", "SNDP", nan_value)
array_SNDP = np.around(2.54 * array_SNDP, decimals=3)
array_SNDP[np.isnan(array_SNDP)] = 0

# Convert unit FRSHTT
#  F R S H T T
#  6 5 4 3 2 1  10
nan_value = np.nan
array_FOG = []
array_RAIN = []
array_SNOW = []
array_HAIL = []
array_THUNDER = []
array_TORNADO = []
for i in range(1, ID_max+1):
    temp_int = int(readFIELDWHERE(station_WBAN+"_GSOD_RAW", "FRSHTT", "ID = " + str(i), nan_value))
    #       F  R  S  H  T  T
    #index  0  1  2  3  4  5
    temp = [0, 0, 0, 0, 0, 0]
    for j in range(5, -1, -1):
        temp[j] = temp_int % 10
        temp_int = round(temp_int / 10)
    array_FOG.append(temp[0])
    array_RAIN.append(temp[1])
    array_SNOW.append(temp[2])
    array_HAIL.append(temp[3])
    array_THUNDER.append(temp[4])
    array_TORNADO.append(temp[5])
array_FOG = np.asarray(array_FOG)
array_RAIN = np.asarray(array_RAIN)
array_SNOW = np.asarray(array_SNOW)
array_HAIL = np.asarray(array_HAIL)
array_THUNDER = np.asarray(array_THUNDER)
array_TORNADO = np.asarray(array_TORNADO)

# Store it to tables of years
# From WBAN_GSOD_RAW to table of years, ex:`1933`

# List of value should be stored, in order
def listOfValue(ID):
    value_list = [0] * 28

    value_list[0] = station_STN
    value_list[1] = station_WBAN
    value_list[2] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "YEARMODA", "ID = " + str(ID), np.nan)
    value_list[3] = array_TEMP_AVG[ID-1]
    value_list[4] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "TEMP_COUNT", "ID = " + str(ID), np.nan)
    value_list[5] = array_DEWP_AVG[ID-1]
    value_list[6] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "DEWP_COUNT", "ID = " + str(ID), np.nan)
    value_list[7] = array_SLP_AVG[ID-1]
    value_list[8] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "SLP_COUNT", "ID = " + str(ID), np.nan)
    value_list[9] = array_STP_AVG[ID-1]
    value_list[10] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "STP_COUNT", "ID = " + str(ID), np.nan)
    value_list[11] = array_VISIB_AVG[ID-1]
    value_list[12] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "VISIB_COUNT", "ID = " + str(ID), np.nan)
    value_list[13] = array_WDSP_AVG[ID-1]
    value_list[14] = readFIELDWHERE(station_WBAN+"_GSOD_RAW", "WDSP_COUNT", "ID = " + str(ID), np.nan)
    value_list[15] = array_MXSPD[ID-1]
    value_list[16] = array_WDSP_MAX[ID-1]
    value_list[17] = array_TEMP_MAX[ID-1]
    value_list[18] = array_TEMP_MIN[ID-1]
    value_list[19] = array_PRCP[ID-1]
    value_list[20] = PRCP_FLAG[ID-1]
    value_list[21] = array_SNDP[ID-1]
    value_list[22] = array_FOG[ID-1]
    value_list[23] = array_RAIN[ID-1]
    value_list[24] = array_SNOW[ID-1]
    value_list[25] = array_HAIL[ID-1]
    value_list[26] = array_THUNDER[ID-1]
    value_list[27] = array_TORNADO[ID-1]

    return value_list

'''
don't touch this part
'''
# print(listOfValue(7111))

# for i in range(1, ID_max+1):
#     list_value = listOfValue(i)
#     print(list_value[2])
#     # And skip February 29
#     if list_value[2][4:6] == "02" and list_value[2][6:8] == "29":
#         continue
#
#     insertVALUES(list_value[2][0:4], list_value)

'''
don't touch this part
'''