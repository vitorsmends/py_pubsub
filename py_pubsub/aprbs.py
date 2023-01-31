import numpy as np
import matplotlib.pyplot as plt

nstep = 1000

# random signal generation

a_range = [-1, 1]
# range for amplitude
a = np.random.rand(nstep) * (a_range[1]-a_range[0]) + a_range[0]

b_range = [1, 100]
# range for frequency
b = np.random.rand(nstep) * (b_range[1]-b_range[0]) + b_range[0]
b = np.round(b)
b = b.astype(int)

b[0] = 0

for i in range(1, np.size(b)):
    b[i] = b[i-1]+b[i]

# Random Signal
i = 0
random_signal = np.zeros(nstep)
while b[i] < np.size(random_signal):
    k = b[i]
    random_signal[k:] = a[i]
    i = i+1

# PRBS
a = np.zeros(nstep)
j = 0
while j < nstep:
    a[j] = 5
    a[j+1] = -5
    j = j+2

i = 0
prbs = np.zeros(nstep)
while b[i] < np.size(prbs):
    k = b[i]
    prbs[k:] = a[i]
    i = i+1

plt.figure(0)
plt.subplot(2, 1, 1)
plt.plot(random_signal, drawstyle='steps', label='APRBS')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(prbs, drawstyle='steps', label='PRBS')
plt.legend()
plt.show()
