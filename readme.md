## Reconhecimentos de padrões 

### Segundo trabalho

### Venancius Michelan e Rafael Soratto

Neste trabalho vocês terão que identificar três possíveis eventos em sinais gravados com o OpenBCI. Os eventos são os seguintes:

    - Mordida ou aperto de mandíbula (jaw clench);
    - Piscar dos olhos (blink);
    - Ritmos alpha: onda evocada no estado de meditação, aumentando as frequências que vão de 8 à 13 Hz.
    - E ritmos beta: onda evocada no estado de concentração, aumentando as frequências que vão de 13 à 32 Hz.

```javascript
eeg_bands = {
        'Delta': (0.5   , 4),
        'Theta': (4     , 8),
        'Alpha': (8     , 13),
        'Beta' : (13    , 32),
        'Gama' : (32    , 100)
        }
```

O código que indica o momento em que um evento inicia e termina, além de nomear o evento ocorrido. 

### Dependencias do projeto

- python3
  - numpy 
  - scipy.signal
  - time
  - mne
  - re
  - pylsl
  
### Execucão

### python3 main.py
### python3 send_data.py

