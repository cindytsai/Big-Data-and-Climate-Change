import matplotlib.pyplot as plt
import getSQLite
import numpy as np
import pandas as pd

every_day = 365
start_year = getSQLite.start_year
end_year = getSQLite.end_year

# TEMP_MAX - TEMP_AVG and TEMP_AVG - TEMP_MIN, square -> sum
def squareDistance(T1, T2, T3, x):
    '''
    (T1 - T2) ** 2 + (T2 - T3) ** 2 = squareDistance
    :param T1: np.array
    :param T2: np.array
    :param T3: np.array
    :param x: np.array, x-axis
    :return x: np.array, cancels out missing value in T1, T2, T3
    :return squareDistance: np.array
    '''

    # Find out np.nan index in T1, then cancel in T1, T2, T3
    nan_index = pd.isna(T1)
    T1 = T1[~nan_index]
    T2 = T2[~nan_index]
    T3 = T3[~nan_index]
    x = x[~nan_index]
    # Find out np.nan index in T2, then cancel in T1, T2, T3
    nan_index = pd.isna(T2)
    T1 = T1[~nan_index]
    T2 = T2[~nan_index]
    T3 = T3[~nan_index]
    x = x[~nan_index]
    # Find out np.nan index in T3, then cancel in T1, T2, T3
    nan_index = pd.isna(T3)
    T1 = T1[~nan_index]
    T2 = T2[~nan_index]
    T3 = T3[~nan_index]
    x = x[~nan_index]

    # (T1 - T2) ** 2 + (T2 - T3) ** 2 = squareDistance
    squareDistance = np.square(T1 - T2) + np.square(T2 - T3)

    return x, squareDistance

# Plot from initial value TEMP_AVG, TEMP_MAX, TEMP_MIN
for year in range(start_year, end_year+1):
# for year in [1933,1941,1967,1969,1973,1975,1995,1999,2009,2011,2015,2017,2018]:
    TEMP_AVG = getSQLite.getField(str(year), "TEMP_AVG")
    TEMP_MAX = getSQLite.getField(str(year), "TEMP_MAX")
    TEMP_MIN = getSQLite.getField(str(year), "TEMP_MIN")
    DAY = np.arange(1, every_day+1)
    DAY, distance2 = squareDistance(TEMP_MAX, TEMP_AVG, TEMP_MIN, DAY)


    # Plot, no storm
    '''
    try:
        plt.figure(figsize=(18,7))
        plt.stem(DAY, distance2)
        plt.title("(T_MAX-T_AVG)**2 + (T_AVG-T_MIN)**2, year = " + str(year), color='b')
        plt.xlabel("DAY")
        plt.ylabel("$^\Delta$T**2")
        plt.xticks([16, 45, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350], \
                   ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

        # plt.show()
        plt.savefig(str(year)+"deltaT^2"+'.png', bbox_inches="tight")
        plt.close()
        print("success", year)

    except:
        print("failed", year)
    '''

    # Get storm data by year,
    # and convert it to coordinate
    # (x, y) = (DAY, value of stem)
    table_name = str(year) + "stormtypeDAY"
    storm_X = getSQLite.getField(table_name, "DAY")
    storm_Y = []

    print("------------------")
    print(year)

    # Find out storm_Y
    for i in range(len(storm_X)):
        # storm_X might not be inside DAY, so check if storm_X[i] is inside DAY
        # storm_X[i] not inside DAY
        if len(np.argwhere(DAY == storm_X[i])) == 0:
            storm_Y.append(0)
        # storm_X[i] inside DAY
        else:
            storm_Y.append(distance2[np.argwhere(DAY == storm_X[i])][0][0])
    storm_Y = np.asarray(storm_Y)


    # storm XY coordinate, where text will be
    storm_XY = np.concatenate(([storm_X], [storm_Y]), axis=0)
    storm_XY = storm_XY.T


    # print(storm_XY)

    # Get the string value of each storm by year
    table_name = str(year) + "stormtype"
    storm_text = getSQLite.getField(table_name, "STORMTYPE")


    # stem Plot, with storm
    # try:
    #     plt.figure(figsize=(18,7))
    #     plt.stem(DAY, distance2)
    #     plt.title("(T_MAX-T_AVG)**2 + (T_AVG-T_MIN)**2, year = " + str(year), color='b')
    #     plt.xlabel("DAY")
    #     plt.ylabel("$^\Delta$T**2")
    #
    #     for i in range(len(storm_text)):
    #         plt.text(storm_XY[i][0], storm_XY[i][1], storm_text[i], fontsize=12, color='r', rotation=90,
    #                  horizontalalignment='left', verticalalignment='bottom')
    #
    #     plt.xticks([16, 45, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350], \
    #                ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
    #     plt.ylim([0, 500])
    #     # Save img
    #     plt.savefig(str(year) + "deltaT^2 (Storm)_ylim500" + '.png', bbox_inches="tight")
    #     plt.close()
    #     print("success", year)
    # except:
    #     print("failed : ", year)

    # hist Plot, with storm count
    # plt.hist(distance2, bins=np.linspace(0, 500, 15), edgecolor='black', linewidth=1.2, label="storm num="+str(len(storm_text)))
    # plt.title("(T_MAX-T_AVG)**2 + (T_AVG-T_MIN)**2 Histogram, year = " + str(year), color='b')
    # plt.xlabel("$^\Delta$T**2")
    # plt.ylabel("num")
    # plt.legend(bbox_to_anchor=(1, 1))
    # plt.savefig(str(year) + "deltaT^2 (Storm)_hist" + '.png', bbox_inches="tight")
    # plt.close()
    # print("success", year)

    # hist Plot, log x scale, with storm count
    plt.hist(distance2, bins=10**np.linspace(0, 2.7, 15), edgecolor='black', linewidth=1.2, label="storm num="+str(len(storm_text)))
    plt.title("(T_MAX-T_AVG)**2 + (T_AVG-T_MIN)**2 Histogram xscale = log, year = " + str(year), color='b')
    plt.xlabel("$^\Delta$T**2")
    plt.ylabel("num")
    plt.ylim([0, 170])
    # plt.xscale('log')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig(str(year) + "deltaT^2 (Storm)_hist_xlog" + '.png', bbox_inches="tight")
    plt.close()
    print("success", year)


