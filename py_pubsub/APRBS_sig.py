
import numpy as np
import matplotlib.pyplot as plt


def APRBS(a_range, b_range, nstep):
    # random signal generation
    # range for amplitude
    a = np.random.rand(nstep) * (a_range[1]-a_range[0]) + a_range[0]
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
    return random_signal


def multiple_aprbs(a_range, b_range, nstep, ninput, type='float', factor=1.0):
    u = np.zeros([ninput, nstep])
    for i in range(ninput):
        u[i, :] = APRBS(a_range, b_range, nstep)*factor
    if type == 'int':
        u = u.astype('int32')
    return u


ninput = 3
nstep = 100
a_range = [0, 4]
b_range = [0, 5]
u = multiple_aprbs(a_range, b_range, nstep, ninput, type='int', factor=100)
plt.figure()
for i in range(ninput):

    plt.plot((u[i, :]), label='M'+str(i), drawstyle='steps')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
plt.legend()
plt.show()
print(int(u[1, 1]))
