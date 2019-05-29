from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np

# Finding relation between sample_rate and frequency (Hz)
sample_rate = 365
f = 10


# Plot sin
t = np.linspace(0, 2, sample_rate, endpoint=False)
x = np.sin(f * 2 * np.pi * t)
plt.plot(t,x)
plt.show()

# apply FFT
X = fftpack.fft(x)
# fftpack.fftfreq span [0, 0.5]
# so multiply sample_rate/2
freqs = fftpack.fftfreq(sample_rate)*(sample_rate/2)



# Plot only the first half, delete the symmetric part
plt.stem(freqs[0:len(x)//2], np.abs(X[0:len(x)//2]))
plt.xlabel("frequency (Hz)")
plt.show()

