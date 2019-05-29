import numpy as np
import matplotlib.pyplot as plt
import getSQLite
import numpy.linalg as LA
import pandas as pd

start_year = getSQLite.start_year
end_year = getSQLite.end_year
total_year = 86
every_day = 365
want_field = "TEMP_AVG"

def diff(y, step):
    '''
    diff
    :param y: np.array
    :param step: int
    :return: np.array
    '''

    diff_array = []

    # index of start of changed y and end of changed y
    start_y = step
    end_y = (len(y) - 1) + 5

    # add np.nan * step in front of y, and at the end of y
    y = np.concatenate((np.array([np.nan] * step), y))
    y = np.concatenate((y, np.array([np.nan] * step)))

    # Create x, same length as y
    x = np.arange(len(y))

    # If meet np.nan inside these (step*2 + 1) point, then append np.nan to diff
    for i in range(start_y, end_y+1):
        # Chop to many pieces, then np.polyfit
        fit_y = y[(i-step):(i+step+1)]
        fit_x = x[(i-step):(i+step+1)]
        try:
            res_y = np.polyfit(fit_x, fit_y, 2)

            # diff = 2ax + b
            diff_val = 2 * res_y[0] * x[i] + res_y[1]
            diff_array.append(diff_val)

        except:
            diff_array.append(np.nan)

    diff_array = np.asarray(diff_array)

    return diff_array


# Get TEMP_AVG full array
z = getSQLite.getField("1933", want_field)
z[z==None] = np.nan
for year in range(start_year+1, end_year+1):
    temp_z = getSQLite.getField(str(year), want_field)
    temp_z[temp_z==None] = np.nan
    z = np.concatenate((z, temp_z))

z_diff_list = diff(z, 5)
z_diff_list = np.reshape(z_diff_list, (86, 365))

# Get SLP_AVG full array
want_field = "SLP_AVG"
p = getSQLite.getField("1933", want_field)
p[p == None] = np.nan
for year in range(start_year + 1, end_year + 1):
    temp_p = getSQLite.getField(str(year), want_field)
    temp_p[temp_p == None] = np.nan
    p = np.concatenate((p, temp_p))

p_diff_list = diff(p, 5)
p_diff_list = np.reshape(p_diff_list, (86, 365))

print(p_diff_list)


#####################################################
DAY = np.arange(1, every_day+1)

for i in range(total_year):

    temp_diff = z_diff_list[i]
    temp_diff = temp_diff / LA.norm(temp_diff)

    pressure_diff = p_diff_list[i]
    pressure_diff = pressure_diff / LA.norm(pressure_diff)

    # Plot
    plt.figure(figsize=(18,7))
    temp, = plt.plot(DAY, temp_diff, 'r.-', label='Temperature diff')
    pres, = plt.plot(DAY, pressure_diff, 'b.-', label='Pressure diff')
    plt.legend(loc='upper right')
    plt.title('Temperature Differential and Pressure Differential, year = '+str(i+start_year), fontsize=16, color='b')
    plt.xlabel("DAY")
    plt.xticks([16, 45, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350], \
               ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

    plt.savefig(str(i+start_year)+"tempDiff and presDiff.png", bbox_inches="tight")
    plt.close()

    plt.show()
