import sqlite3
import numpy as np

# TODO: file dependent
database_name = "23119_GSOD"

# Connect to database
conn = sqlite3.connect(database_name+".db")
cursor = conn.cursor()


def getField(table_name, field_name):
    '''
    @:param table_name string
    @:param field_name string
    @:return array     np.array
    '''

    sql_cmd = "SELECT " + field_name + " FROM " + "`" + table_name + "`"

    try:
        cursor.execute(sql_cmd)

    except:
        print("(getField) NO TABLE, or NO FIELD : ", table_name, ", ", field_name)
        return np.array([np.nan])

    else:
        array = []
        for value in cursor.fetchall():
            array.append(value[0])
        array = np.asarray(array)
        return array


def getFieldWhere(table_name, field_name, where):
    '''
    @:param table_name string
    @:param field_name string
    @:param where      string    EX: "ID = 1"
    @:return value     dependents on the field
    '''

    sql_cmd = "SELECT " + field_name + " FROM " + "`" + table_name + "`" + " WHERE " + where

    try:
        cursor.execute(sql_cmd)

    except:
        print("(getFieldWhere) NO TABLE, or NO FIELD : ", table_name, ", ", field_name)
        return np.nan

    else:
        value = np.nan
        for row in cursor.fetchall():
            value = row[0]
        return value


def getTableIDMax(table_name):
    '''
    @:param table_name string
    @:return id_max    integer  => 0 means no ID yet
    '''

    sql_cmd = "SELECT ID FROM " + "`" + table_name + "`"

    try:
        cursor.execute(sql_cmd)

    except:
        print("(getTableIDMax) NO TABLE : ", table_name)
        return np.nan

    else:
        try:
            id_max = cursor.fetchall()[-1][0]
        except:
            id_max = 0

        return id_max


def createTable(table_name):
    '''
    @:param table_name string
    '''

    sql_cmd = "CREATE TABLE IF NOT EXISTS " + "`" + table_name + "`" + " (ID INTEGER PRIMARY KEY AUTOINCREMENT)"
    cursor.execute(sql_cmd)
    conn.commit()


def createTableColumn(table_name, add_field_name, add_field_declare):
    '''
    @:param table_name        string
    @:param add_field_name    string
    @:param add_field_declare string
    '''

    sql_cmd = "ALTER TABLE " + "`" + table_name + "`" + " ADD COLUMN " + add_field_name + " " + add_field_declare

    try:
        cursor.execute(sql_cmd)
        conn.commit()

    except:
        print("(createTableColumn) NO TABLE : ", table_name)
        print("(createTableColumn) or WRONG DECLARATION or EXISTS ALREADY: ", add_field_name, " ", add_field_declare)


def insertField(table_name, field_name, value_list):
    '''
    @:param table_name string
    @:param field_name string, single field at a time
    @:param value_list list or array, elements depends on the field
    '''

    # Add value from the start or from the existing field from the last one

    try:
        for i in range(len(value_list)):
            sql_cmd = "INSERT INTO " + "`" + table_name + "`" + " (" + field_name + ") VALUES " \
                      "(" + str(value_list[i]) + ")"
            cursor.execute(sql_cmd)
            conn.commit()

    except:
        try:
            # Check if table have field field_name
            field_info = [i[1] for i in cursor.execute("PRAGMA table_info(" + table_name + ")")]
        except:
            print("(insertField) NO TABLE : ", table_name)
        else:
            have_field = 0
            for j in range(len(field_info)):
                if field_name == field_info[j]:
                    have_field = 1
                    break
            if have_field == 0:
                print("(insertField) NO FIELD : ", field_name)

# def replaceField(table_name, field_name, value_list):
#     '''
#     Use when ID is not zero, which means there are other existing fields
#     :param table_name: string
#     :param field_name: string
#     :param value_list: np.array or list
#     :return:
#     '''
#
#     try:
#         for ID in range(1, len(value_list) + 1):
#             # ID starts from 1
#             # sql_cmd = "INSERT OR REPLACE INTO " + "`" + table_name + "`" + " (ID," + field_name + ") " + "VALUES " \
#             #           "(" + str(ID) + "," + str(value_list[ID - 1]) + ")"
#             sql_cmd = "INSERT OR REPLACE INTO " + "`" + table_name + "`" + " (ID," + field_name + ") " + "VALUES " \
#                       "(" + str(ID) + "," + str(value_list[ID - 1]) + ")"
#             cursor.execute(sql_cmd)
#             conn.commit()
#
#     except:
#         try:
#             # Check if table have field field_name
#             field_info = [i[1] for i in cursor.execute("PRAGMA table_info(" + table_name + ")")]
#         except:
#             print("(replaceField) NO TABLE : ", table_name)
#         else:
#             have_field = 0
#             for j in range(len(field_info)):
#                 if field_name == field_info[j]:
#                     have_field = 1
#                     break
#             if have_field == 0:
#                 print("(replaceField) NO FIELD : ", field_name)





start_year = int(getFieldWhere(database_name+"_RAW", "YEARMODA", "ID = 1")[0:4])
end_year = int(getFieldWhere(database_name+"_RAW", "YEARMODA", "ID = " + str(getTableIDMax(database_name+"_RAW")))[0:4])
