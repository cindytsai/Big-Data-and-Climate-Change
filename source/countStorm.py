import numpy as np
import datetime
import getSQLite
import sqlite3

database_name = "23119_GSOD"
conn = sqlite3.connect(database_name+".db")
cursor = conn.cursor()

# TODO: File dependent
NAME_list = ["Riverside1.csv", "Riverside2.csv", "Riverside3.csv", "Riverside4.csv"]


start_year = getSQLite.start_year
end_year = getSQLite.end_year


yearmoda_list = []
stormtype_list = []


def findDateStorm(NAME, date_list, storm_list):
    data_file = open(NAME, "r", encoding="utf-8")
    data_ori = data_file.read().split("\n")

    for i in range(1, len(data_ori)-1):
        try:
            # Try if index[3], index[5] out of range
            index = data_ori[i].split(",")
            
            # Find date
            date_ori = index[3]
            
            try:
                # Try if it is mo/da/year format
                mo = date_ori[0:2]
                da = date_ori[3:5]
                year = date_ori[6:10]
                
                check = datetime.datetime(int(year), int(mo), int(da))

                date_list.append(year+mo+da)
                storm_list.append(index[5])
            
            except:
                print("line : ", i)

        except:
            print("line : ", i)

    data_file.close()

    return date_list, storm_list


def checkDate(moda):
    '''
    @:param moda string, "moda" format
    @:return check   boolean
    '''

    # Check if it is a valid date
    mo = int(moda[0:2])
    da = int(moda[2:4])
    try:
        # 1933 has no 02/29, skip it
        newDate = datetime.datetime(1933, mo, da)
        check = True
    except ValueError:
        check = False

    return check


# Create every_day list, so nextDate can produce next day.
every_day = []
for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
    for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16",
                "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
        # Skip invalid date and 02/29
        date = month + day
        if checkDate(date) == False:
            break
        every_day.append(date)


def parseDate(date_string):
    '''
    Parse date_string to DAY
    :param date_string: string, EX: 19500101
    :return year:       string,     1950
    :return day:        int,        1
    '''

    year = date_string[0:4]
    moda = date_string[4:8]

    for i in range(len(every_day)):
        if moda == every_day[i]:
            day = i + 1
            break
    return year, day


## Processing

# Parsing .csv data
for i in range(len(NAME_list)):
    yearmoda_list, stormtype_list = findDateStorm(NAME_list[i], yearmoda_list, stormtype_list)

'''
# Drop table if needed.
for year in range(start_year, end_year+1):
    table_name = str(year) + "stormtypeDAY"
    cursor.execute("DROP TABLE " + "`"+table_name+"`")
    conn.commit()

    table_name = str(year) + "stormtype"
    cursor.execute("DROP TABLE " + "`"+table_name+"`")
    conn.commit()

    print("DROP TABLE : ", year)
'''


#Create table and column
for year in range(start_year, end_year+1):
    table_name = str(year) + "stormtypeDAY"
    getSQLite.createTable(table_name)
    getSQLite.createTableColumn(table_name, "DAY", "INTEGER")

    table_name = str(year) + "stormtype"
    getSQLite.createTable(table_name)
    getSQLite.createTableColumn(table_name, "STORMTYPE", "TEXT")

    print("CREATE TABLE : ", year)


# Put data into table
for i in range(len(yearmoda_list)):
    # year string; day int
    year, day = parseDate(yearmoda_list[i])

    # insert into TABLE YEARstormtypeDAY; FIELD DAY
    table_name = str(year) + "stormtypeDAY"
    getSQLite.insertField(table_name, "DAY", [day])


    # insert into TABLE YEARstormtype; FIELD STORMTYPE
    table_name = str(year) + "stormtype"
    getSQLite.insertField(table_name, "STORMTYPE", [stormtype_list[i]])
    print(year)
