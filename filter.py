import numpy as np


def calc_filter(number_freq):

    filtering_array = 2 * np.arange(number_freq + 1) / np.float32(2 * number_freq)
    # w = 2 * np.pi * np.arange(number_freq + 1) / np.float32(2 * number_freq)
    # filtering_array[1:] *= (1.0 + np.cos(w[1:])/2.0)
    filtering_array = np.concatenate((filtering_array, filtering_array[number_freq - 1:0:-1]), axis=0)

    return filtering_array


def filter_projection(sinogram):

    number_angles, number_offsets = sinogram.shape
    number_freq = 2 * int(2**(int(np.ceil(np.log2(number_offsets)))))

    filter_array = calc_filter(number_freq)

    print(sinogram)

    padded_sinogram = np.concatenate((sinogram, np.zeros((number_angles, 2 * number_freq - number_offsets))), axis=1)

    for i in range(number_angles):
        padded_sinogram[i, :] = np.real(np.fft.ifft(np.fft.fft(padded_sinogram[i, :]) * filter_array))

    # sinogram[:, :] = padded_sinogram[:, :number_offsets]

    return padded_sinogram[:, :number_offsets]

