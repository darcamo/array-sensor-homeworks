from matplotlib import pyplot as plt
import numpy as np
from pyphysim import modulators
from pyphysim.util.conversion import dB2Linear
from math import sqrt
from itertools import product
from pyphysim.util.misc import randn_c
import json


def calc_a_phi_vect(M, phi):
    return np.exp(1j * np.arange(M)[:, np.newaxis] * phi)


def calc_mvdr_spectrum(steering_angles, Rxx):
    """Compute the MVDR spectrum
    """
    Rxx_inv = np.linalg.inv(Rxx)
    mvdr_spectrum = np.empty_like(steering_angles)
    M = Rxx.shape[0]

    for i, mu in enumerate(steering_angles):
        a = calc_a_phi_vect(M, mu)
        mvdr_spectrum[i] = np.linalg.norm(1./(a.T.conj() @ Rxx_inv @ a))
    return mvdr_spectrum


def calc_fourier_spectrum(steering_angles, Rxx):
    fourier_spectrum = np.empty_like(steering_angles)
    M = Rxx.shape[0]
    for i, mu in enumerate(steering_angles):
        a = calc_a_phi_vect(M, mu)
        a_H = a.T.conj()
        fourier_spectrum[i] = np.linalg.norm(a_H @ Rxx @ a)
    return fourier_spectrum

def calc_music_spectrum(steering_angles, U0):
    music_spectrum = np.empty_like(steering_angles)
    U0_H = U0.T.conj()
    M = U0.shape[0]
    for i, mu in enumerate(steering_angles):
        a = calc_a_phi_vect(M, mu)
        a_H = a.T.conj()
        music_spectrum[i] = np.linalg.norm((a_H @ a) / (a_H @ U0 @ U0_H @ a))

    return music_spectrum


def simulate_and_compute_Rxx_U0(M, N, SNR, beam_sep):
    """
    Simulate and generate Rxx and U0 considering that three wavefronts were
    sent.

    M : int
    N : int
    SNR : float
    beam_sep : float
        Normalized beamwidth separation between the wavefronts. This separation
        is normalized by the beamwidth.
    """
    qpsk = modulators.QPSK()

    d = 3  # Number of inpinging waves
    mu_b = 2 * np.pi / M
    mu = np.array([-beam_sep * mu_b, 0, beam_sep * mu_b])  # Standard beamwidth

    data = np.random.randint(4, size=(d, N))
    modulated_data = qpsk.modulate(data) / sqrt(d)
    noise_power = 1./dB2Linear(SNR)
    noise = sqrt(noise_power) * randn_c(M, N)
    steering_vec = calc_a_phi_vect(M, mu)
    received_data = steering_vec @ modulated_data + noise

    # Covariance matrix of the received Data
    Rxx = received_data @ received_data.T.conj()
    U, S, V_H = np.linalg.svd(Rxx)
    U0 = U[:, d:]

    return Rxx, U0


def plot_spectrum(steering_angles, spectrum, filename=None):
    fig, ax = plt.subplots()
    ax.plot(steering_angles, spectrum)[0]
    # ax.plot(steering_angles, music_spectrum)[0]
    if isinstance(filename, str):
        fig.savefig(filename, format='png')
    else:
        plt.show()


def main(M, N, SNR, sep):
    Rxx, U0 = simulate_and_compute_Rxx_U0(M, N, SNR, sep)

    mu_b = 2.*np.pi/M
    steering_angles = np.linspace(-3 * mu_b, 3 * mu_b, 200)

    # MVDR Spectrum
    mvdr_spectrum = calc_mvdr_spectrum(steering_angles, Rxx)
    # MUSIC Spectrumz
    music_spectrum = calc_music_spectrum(steering_angles, U0)
    # Fourier Spectrum
    fourier_spectrum = calc_fourier_spectrum(steering_angles, Rxx)

    return steering_angles/mu_b, mvdr_spectrum, music_spectrum, fourier_spectrum


def simulate():
    SNR = [0, 10, 20]
    sep = np.arange(0, 2.05, 0.1)

    data = []

    for snr, s in product(SNR, sep):
        steering_angles, mvdr_spectrum, music_spectrum, fourier_spectrum = main(M=12, N=100, SNR=snr, sep=s)
        # plot_spectrum(steering_angles, mvdr_spectrum, 'mvdr_snr_{0}_sep_{1}.png'.format(snr, s))
        # plot_spectrum(steering_angles, music_spectrum, 'music_snr_{0}_sep_{1}.png'.format(snr, s))
        # plot_spectrum(steering_angles, fourier_spectrum, 'fourier_snr_{0}_sep_{1}.png'.format(snr, s))

        data.extend(
            [{"angle": i, "mvdr": j, "music": l, "fourier": m, "snr": snr, "sep": s}
             for i, j, l, m in zip(steering_angles, mvdr_spectrum,
                                   music_spectrum, fourier_spectrum)])

    return data


if __name__ == '__main__':
    # # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # # xxxxxxxxxxxxxxx Simulate and save data xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    data = simulate()

    # Save data to a json file
    json_filename = "static/plotdata.json"
    fp = open(json_filename, 'w')
    json.dump(data, fp)


    # # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # # xxxxxxxxxxxxxxx Plot data xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # json_filename = "static/plotdata.json"
    # data = json.load(open(json_filename))

    # fig, ax = plt.subplots()

    # ax.plot(steering_angles, spectrum)[0]
