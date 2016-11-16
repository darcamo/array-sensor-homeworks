import numpy as np


def lms(w0, u, d, s):
    """
    Find the LMS filter coefficients.

    Parameters
    ----------
    w0 : np.ndarray
        Init weight vector with M taps. Dimension: (M,)
    u : np.ndarray
        Input data vector. Dimension: (N,)
    d : Desired Output data vector. Dimension: (N,)
    s : Step size.
    """
    N = u.size
    M = w0.size
    w = w0
    x = np.zeros_like(w0)
    for k in range(N):
        x = np.hstack([u[k], x[:-1]])
        ek = d[k] - w.conj() @ x
        dw = s * ek.conj() * x
        w = w + dw

    return w


# if __name__ == '__main__':
pilots = np.array(
    [-1, -1, -1, +1, +1, -1, -1, -1, +1, +1, +1, +1, -1, +1, +1, -1, +1, -1])
N = pilots.size
M = 5  # Number of filter coefficients
w0 = np.zeros(M)
d = pilots
step = 0.0015

h = np.array([4, -5])  # A channel with 2 taps

# Transmit pilots through the channel
u = np.convolve(pilots, h)[:N]  # Don't include elements after we finished transmission

# Fild filter coefficients using LMS algorithm
w = lms(w0, u, pilots, step)


# Lh = 2  # Channel memory
# Lp = pilots.size  # Number of trainning symbols
# LD = 150  # Number of data symbols
# LG = Lh + M  # Number of transmitted zeroes (guard interval)
