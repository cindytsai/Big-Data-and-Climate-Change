from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np

# Finding relation between sample_rate and frequency (Hz)

sample_rate = 365
f = 10

t = np.linspace(0, 2, sample_rate, endpoint=False)
x = np.sin(f * 2 * np.pi * t)
# plt.plot(t,x)
# plt.show()
print("x")
print(len(x))
print("t")
print(t)

X = fftpack.fft(x)
# fftpack.fftfreq span [0, 0.5]
# so multiply sample_rate/2
freqs = fftpack.fftfreq(sample_rate)*(sample_rate/2)


print("freqs")
print(freqs)
print("len freqs")
print(len(freqs))


# Plot
plt.stem(freqs[0:len(x)//2], np.abs(X[0:len(x)//2]))
plt.xlabel("frequency (Hz)")
# plt.stem(freqs, np.abs(X))
plt.show()

print("------------------------")
# test_f = np.arange(0, len(x)) * (sample_rate//2) / len(x)
# print(test_f)
# plt.plot(test_f[0:sample_rate//2], np.abs(X)[0:sample_rate//2])
# plt.show()
