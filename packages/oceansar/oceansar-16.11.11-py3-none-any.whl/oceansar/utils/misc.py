
import numpy as np

def get_parFile(parfile=None):
    """Mini gui to get filename
    """
    def _test(out_q):
        out_q.put('hola')

    if (parfile is None):
        #output_queue = multiprocessing.Queue()
        #p = multiprocessing.Process(target=_get_parFile, args=(output_queue,))
        #p.start()
        #parfile = output_queue.get()
        #p.join()
        parfile = _get_parFile(1)
    return parfile


def _get_parFile(out_q):
    from tkinter import filedialog as tkfiledialog
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    root.deiconify()
    root.lift()
    root.focus_force()
    parfile = tkfiledialog.askopenfilename(parent=root)
    root.destroy()
    # out_q.put(parfile)
    return parfile


def factorize(n):
    """ Prime factorize a number

        :param n: Number

        :returns: Array with prime factors
    """
    result = np.array([])
    for i in np.append(2, np.arange(3, n + 1, 2)):
        s = 0
        while np.mod(n, i) == 0:
            n /= i
            s += 1
        result = np.append(result, [i]*s)
        if n == 1:
            return result


def nearest_power2(values):
    return (2**np.ceil(np.log2(values))).astype(int)


def optimize_fftsize(values, max_prime=2):
    """ Returns 'good' dimensions for FFT algorithm

        :param value: Input value/s
        :param max_prime: Maximum prime allowed (FFT is optimal for 2)

        :returns: Nearest 'good' value/s
    """
    # Force array type (if scalar was given)
    if np.isscalar(values):
        values = np.array([values], dtype=np.int)

    if max_prime == 2:
        good_values = nearest_power2(values)
        return good_values if len(good_values) > 1 else good_values[0]

    good_values = np.array([], dtype=np.int)
    for value in values:
        best_value = value
        while (np.max(factorize(best_value)) > max_prime):
            best_value += 1
        good_values = np.append(good_values, best_value)

    return good_values if len(good_values) > 1 else good_values[0]


def balance_elements(N, size):
    """ Divide N elements in size chunks
        Useful to balance arrays of size N not multiple
        of the number of processes

        :param N: Number of elements
        :param size: Number of divisions

        :returns: (counts, displ) vectors
    """
    # Counts
    count = np.round(N/size)
    counts = count*np.ones(size, dtype=np.int)
    diff = N - count*size
    counts[:diff] += 1

    # Displacements
    displ = np.concatenate(([0], np.cumsum(counts)[:-1]))

    return counts, displ

def smooth(data, window_len=11, window='flat', axis=None):
    """ Smooth the data using a window with requested size.

        This method is based on the convolution of a scaled window with the signal.
        Works with 1-D and 2-D arrays.

        :param data: Input data
        :param window_len: Dimension of the smoothing window; should be an odd integer
        :param window: Type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'.
                       Flat window will produce a moving average smoothing.
        :param axis: if set, then it smoothes only over that axis

        :returns: the smoothed signal
    """

    if data.ndim > 2:
        raise ValueError('Arrays with ndim > 2 not supported')

    if window_len < 3:
        return data

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError('Window type not supported')

    # Calculate Kernel
    if window == 'flat':
        w = np.ones(window_len)
    else:
        w = eval('np.' + window + '(window_len)')

    # Smooth
    if data.ndim > 1:
        if axis is None:
            w = np.sqrt(np.outer(w, w))
        elif axis == 0:
            w = w.reshape((w.size, 1))
        else:
            w = w.reshape((1, w.size))

    y = signal.fftconvolve(data, w/w.sum(), mode='same')

    return y


def db(a, linear=False):
    """ Mini routine to convert to dB"""
    if linear:
        return 20 * np.log10(np.abs(a))
    else:
        return 10 * np.log10(np.abs(a))


def db2lin(a, amplitude=False):
    """ Mini routine to convert dB to linear"""
    if amplitude:
        return 10**(a/20)
    else:
        return 10**(a/10)