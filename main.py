from pylsl import StreamInfo, StreamInlet, resolve_stream
import re
import mne
from time import sleep
import numpy as np
from scipy.signal import welch

# eeg_bands = {'Delta': (0, 4),
             # 'Theta': (4, 8),
             # 'Alpha': (8, 12),
             # 'Beta': (12, 30),
             # 'Gamma': (30, 45)}

eeg_bands = {
        'Delta': (0.5   , 4),
        'Theta': (4     , 8),
        'Alpha': (8     , 13),
        'Beta' : (13    , 32),
        'Gama' : (32    , 100)
        }

window_size = 10
chunk_size = 250

def main():
    print("Looking for stream")
    
    inlet = StreamInlet(resolve_stream('type', 'EEG')[0])

    chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)
    buffer = np.array(chunk)

    print("Filling buffer")
    for i in range(window_size - 2):
        chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)
        buffer = np.concatenate((buffer, chunk))
        print(i)

    print(buffer.shape)
    print("Processing")
    while True:
        chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)

        buffer = np.concatenate((buffer, chunk))

        f, psd = welch(buffer, fs=250., nperseg=8)

        power = {band: np.mean(psd[np.where((f >= lf) & (f <= hf))]) for band, (lf, hf) in eeg_bands.items()}

        print(power)

        print(buffer.shape)
        buffer = np.delete(buffer, slice(chunk_size), axis=0)
        print(buffer.shape)

if __name__ == '__main__':
    main()
