## Reconhecimentos de padrões 

### Segundo trabalho

### Venancius Michelan e Rafael Soratto

Neste trabalho vocês terão que identificar três possíveis eventos em sinais gravados com o OpenBCI. Os eventos são os seguintes:

    - Mordida ou aperto de mandíbula (jaw clench);
    - Piscar dos olhos (blink);
    - Ritmos alpha: onda evocada no estado de meditação, aumentando as frequências que vão de 8 à 13 Hz.
    - E ritmos beta: onda evocada no estado de concentração, aumentando as frequências que vão de 13 à 32 Hz.

O código que indica o momento em que um evento inicia e termina, além de nomear o evento ocorrido. 

### Dependencias do projeto

- python3
  - numpy 
  - scipy.signal
  - time
  - mne
  - re
  - pylsl
  
Faixas de frequências

```python
eeg_bands = {
        'Delta': (0.1   , 3),
        'Theta': (4     , 8),
        'Alpha': (8     , 12),
        'Beta' : (13    , 30),
        'Gama' : (30    , 100)
}

window_size = 5
chunk_size = 250
```

Algoritmo
```python
def main():
    alpha = False;
    print("Looking for stream")
    
    inlet = StreamInlet(resolve_stream('type', 'EEG')[0])

    chunk, timestamp = inlet.pull_chunk(timeout=3, max_samples=chunk_size)
    buffer = np.array(chunk).transpose()

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

        freqs, psd = welch(buffer, fs=250., nperseg=4*250)
        psd = np.average(psd, axis=0);

        freq_res = freqs[1] - freqs[0] 

        total_power = simps(psd, dx=freq_res)

        band_power = []
        for band in eeg_bands:
            idx = np.logical_and(freqs >= eeg_bands[band][0], freqs <= eeg_bands[band][1])
            tmp = simps(psd[idx], dx=freq_res)
            band_power.append(tmp)
            print(band, tmp, tmp/total_power)

        print()

        if alpha:
            if band_power[2] < band_power[1] or band_power[2] < band_power[3]:
                alpha = False
            else:
                print("Concentração")
        else:
            if band_power[2] / band_power[1] >= 1.3 and band_power[2] / band_power[3] >= 1.3:
                alpha = True

        buffer = np.delete(buffer, slice(250), axis=1)
```

  
## Execucão

-  python3 main.py
-  python3 send_data.py


# Referências
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#scipy.signal.welch
    
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#scipy.signal.welch

