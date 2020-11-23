#https://raphaelvallat.com/bandpower.html
from pylsl import StreamInfo, StreamInlet, resolve_stream
import re
import mne
from time import sleep
import numpy as np
from scipy.signal import welch
from scipy.integrate import simps

# eeg_bands = {'Delta': (0, 4),
             # 'Theta': (4, 8),
             # 'Alpha': (8, 12),
             # 'Beta': (12, 30),
             # 'Gamma': (30, 45)}

# eeg_bands = {
        # 'Delta': (0.5   , 4),
        # 'Theta': (4     , 8),
        # 'Alpha': (8     , 13),
        # 'Beta' : (13    , 32),
        # 'Gama' : (32    , 100)
        # }

#https://books.google.pt/books?id=e-Ex6VHd1UEC&pg=PA111&dq=alpha+8-12+Hz&hl=en&sa=X&ved=0ahUKEwi_1tj098LhAhWy34UKHRMeA2oQ6AEIKDAA#v=onepage&q=alpha%208-12%20Hz&f=false
eeg_bands = {
        'Delta': (0.1   , 3),
        'Theta': (4     , 8),
        'Alpha': (8     , 12),
        'Beta' : (13    , 30),
        'Gama' : (30    , 100)
}

window_size = 5
chunk_size = 250

def detect_alpha(band_power):
        print("Concentração")


def main():
    alpha = False;
    print("Looking for stream")
    
    inlet = StreamInlet(resolve_stream('type', 'EEG')[0])

    chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)
    buffer = np.array(chunk).transpose()

    # print("first buffer", buffer.shape, buffer)

    print("Filling buffer")
    for i in range(window_size - 2):
        chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)
        chunk = np.array(chunk).transpose()
        buffer = np.hstack((buffer, chunk))
        print(i)

    print(buffer.shape)
    print("Processing")
    while True:
        chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)
        chunk = np.array(chunk).transpose()

        buffer = np.hstack((buffer, chunk))
        #print("buffer", buffer.shape, buffer)

        freqs, psd = welch(buffer, fs=250., nperseg=4*250)
        psd = np.average(psd, axis=0);
        #print("freqs", freqs.shape, freqs)
        #print("psd", psd.shape, psd)

        freq_res = freqs[1] - freqs[0] 
        #print("freq_res", freq_res)

        total_power = simps(psd, dx=freq_res)

        band_power = []
        for band in eeg_bands:
            idx = np.logical_and(freqs >= eeg_bands[band][0], freqs <= eeg_bands[band][1])
            #print("idx", idx.shape, idx)
            # print("min:", eeg_bands[band][0], "max:", eeg_bands[band][1])
            # print(freqs >= eeg_bands[band][0])
            # print(freqs <= eeg_bands[band][1])

            # print("psd", psd.shape)

            # print("freqs:", freqs)
            # print(psd,idx,freq_res)
            # print(psd.shape)
            tmp = simps(psd[idx], dx=freq_res)
            band_power.append(tmp)
            print(band, tmp, tmp/total_power)
        print()
        #power = {band: np.mean(psd[np.where((freqs >= lf) & (freqs <= hf))]) for band, (lf, hf) in eeg_bands.items()}
        #print(power)

        #print(band_power)

        if alpha:
            if band_power[2] < band_power[1] or band_power[2] < band_power[3]:
                alpha = False
            else:
                print("Concentração")
        else:
            if band_power[2] / band_power[1] >= 1.3 and band_power[2] / band_power[3] >= 1.3:
                alpha = True

        #print(buffer.shape)
        buffer = np.delete(buffer, slice(250), axis=1)
        #print(buffer.shape)

if __name__ == '__main__':
    main()
