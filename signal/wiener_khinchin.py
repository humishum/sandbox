''' WIP on wiener khinchin, 
intuitively, something still feels off, need to revisit this 
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

np.random.seed(0)
fs_hz = 1000  
dt = 1/fs_hz
N = fs_hz * 10
noise = np.random.normal(0, 1, N)

# Autocorr
autocorr = np.correlate(noise, noise, mode='full') / N
lags = np.arange(-N+1, N) * dt
autocorr_positive = autocorr[N-1:]

# PSD via wiener khinchin
psd_wk = np.real(np.fft.rfft(autocorr_positive)) * dt
freqs = np.fft.rfftfreq(len(autocorr_positive), dt)

# Welch's 
freqs_welch, psd_welch = welch(noise, fs=fs_hz, nperseg=2048)

plt.figure(figsize=(12,5))
plt.semilogy(freqs, psd_wk, label='PSD via autocorr (W-K)')
plt.semilogy(freqs_welch, psd_welch, '--', label='PSD(Welch)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (Power/Hz)')
plt.legend()
plt.title('PSD estimation via Wiener–Khinchin theorem')
plt.grid(True)
plt.tight_layout()
plt.show()
