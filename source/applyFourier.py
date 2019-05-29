from scipy import fftpack
import getSQLite
import matplotlib.pyplot as plt
import numpy as np

# TODO: field dependent
want_field = "TEMP_AVG"
table_name_minor = "FFT"


start_year = getSQLite.start_year
end_year = getSQLite.end_year
sample_rate = 365


# Apply fftpack.fft, and write it in to sqlite database.
for year in range(start_year, end_year+1, 1):
    try:
        x = getSQLite.getField(str(year), want_field)
        x = x / np.linalg.norm(x)
        xf = fftpack.fft(x)
        # Magnitude of xf
        value_list = np.abs(xf)[0:sample_rate//2]
        print("fft ", year)

    except:
        # If there is missing value inside array, fft can't work
        nan_array = [np.nan] * (sample_rate//2)
        value_list = np.asarray(nan_array)
        print("nan ", year)

    finally:
        # Create table, and insert value
        # Table name -> YEAR"want_field"_"table_name_minor"
        # Field name -> table_name_minor
        table_name = str(year) + want_field + "_" + table_name_minor
        getSQLite.createTable(table_name)
        getSQLite.createTableColumn(table_name, table_name_minor, "REAL")
        getSQLite.insertField(table_name, table_name_minor, value_list)


# Write the coorelate frequency into database
xf_freqs = fftpack.fftfreq(sample_rate) * (sample_rate/2)
getSQLite.createTable("xf_freq_" + str(sample_rate))
getSQLite.createTableColumn("xf_freq_" + str(sample_rate), "FREQ", "REAL")
getSQLite.insertField("xf_freq_" + str(sample_rate), "FREQ", xf_freqs[0:sample_rate//2])

'''
# Dealing with some missing value
nan_value = [None] * (sample_rate//2)
print(nan_value)

for missing in [1933, 1941, 1999, 2000, 2001, 2002, 2003, 2004, 2015, 2018]:
    getSQLite.insertField(str(missing) + want_field + "_" + table_name_minor, table_name_minor, nan_value)
    print(missing)
    ID = getSQLite.getTableIDMax(str(missing) + want_field + "_" + table_name_minor)
    print(ID)

print("done")
'''

# Plot
xf_mag = getSQLite.getField("2017TEMP_AVG_FFT", "FFT")
xf_mag_log = np.log(xf_mag)

ax = plt.stem(xf_freqs[0:len(xf_mag)//2], xf_mag_log[0:len(xf_mag)//2])
plt.xlabel("Frequency (Hz)", fontsize=14)
plt.ylabel("log10(magnitude)", fontsize=14)
plt.title("log10(magnitude), year = 2017", fontsize=16, color='b')
plt.show()

