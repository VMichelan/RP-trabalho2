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

def main():
    print("Looking for stream")
    
    inlet = StreamInlet(resolve_stream('type', 'EEG')[0])

    while True:
        chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=250)
        print(chunk)

        arr = np.array(chunk)

        f, psd = welch(arr, fs=250., nperseg=250)

        power = {band: np.mean(psd[np.where((f >= lf) & (f <= hf))]) for band, (lf, hf) in eeg_bands.items()}

        print(power)

if __name__ == '__main__':
    main()
