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

# resaultados

```shell 
Gama 774.5190794100342 0.05146282066057656

Delta 1150.1193728074547 0.27204333293261407
Theta 11.778440607956389 0.0027860118831975664
Alpha 28.487703101077955 0.006738335065424071
Beta 23.83811090292566 0.005638544393021765
Gama 773.0758009122117 0.18285938178429134

Delta 168.9158757724266 0.14197933021392603
Theta 9.358376946024944 0.007866022566618697
Alpha 25.617992227632996 0.02153276215910682
Beta 21.417515903178383 0.018002124127611194
Gama 760.3226415724254 0.6390761016588673

Delta 127.6589385450456 0.11494559625814581
Theta 10.38281380115195 0.009348806568602274
Alpha 29.642438175167477 0.026690396845087068
Beta 20.635770804607418 0.018580688562948207
Gama 764.6924326467208 0.6885379796077007

Delta 151.75683072630102 0.13403054163071207
Theta 8.931259204313832 0.00788802390554274
Alpha 23.111723483235398 0.02041210798651997
Beta 19.924823738935896 0.01759746104900184
Gama 761.5962313286996 0.6726363149543796

Meditação
Delta 116.41375071734761 0.10964125904822875
Theta 11.390198940923213 0.010727562208048718
Alpha 18.51079768977919 0.01743391267945804
Beta 19.322279950369467 0.01819818611106016
Gama 753.0146554377616 0.7092072405125357

Delta 71.37217817850896 0.07284819085291136
Theta 10.145387240202911 0.010355198969863264
Alpha 21.041011620384705 0.021476150362490343
Beta 20.77567307733844 0.021205324484427284
Gama 757.3911972772884 0.7730544295786209

Delta 102.88371338646176 0.10149510176079135
Theta 9.80256794381879 0.00967026362314288
Alpha 24.390701478590405 0.024061502516805226
Beta 20.392511823051127 0.020117276044111634
Gama 759.8612406983231 0.7496054663099456

Delta 92.21182421620559 0.09066774303381261
Theta 11.011390052025613 0.010827005019890723
Alpha 40.33584364301011 0.03966042248444928
Beta 19.357014389950308 0.01903288240448223
Gama 752.1629152093549 0.7395679946192849

Delta 98.78079891465835 0.0968344723598427
Theta 11.063062345797665 0.010845081399522772
Alpha 45.5007567597374 0.04460423302112909
Beta 21.59900477702678 0.021173428986822486
Gama 759.3070284810406 0.7443460294910688

Meditação
Delta 84.08190469597895 0.08108068768376975
Theta 11.20144307893239 0.010801619101926401
Alpha 63.48008023675635 0.06121422413571028
Beta 21.992998212915285 0.021207980787052376
Gama 758.3102242926816 0.7312431216395204

Meditação
Delta 85.8018249277025 0.08194067376328493
Theta 11.28328702767086 0.010775530032035179
Alpha 79.92693958687414 0.0763301629901732
Beta 23.074571747993726 0.022036197451779458
Gama 756.4631374295335 0.7224216875374581

Meditação
Delta 62.181976001946325 0.06141913660447296
Theta 11.22041406672022 0.011082763666131621
Alpha 80.27049157503758 0.07928574491105128
Beta 21.60148324395083 0.021336479403258623
Gama 756.9639621287845 0.7476776388256894

Meditação
Delta 77.36116210523255 0.07472712093118104
Theta 11.858177225735243 0.01145442259987662
Alpha 81.92752558731809 0.07913800601686999
Beta 21.22610589376663 0.020503386180573787
Gama 754.8365952160257 0.7291354472837432
```

# Referências
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#scipy.signal.welch
    
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#scipy.signal.welch

