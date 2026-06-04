# Display Controller

Programme qui reçoit les pixels en osc est les envoie à l'arduino.

## installation

```bash
python3 -m pip install -r requirements.txt --break-system-packages
```

## usage
Lister les ports séries disponibles:
```bash
python3 main.py -l
```

Démarrer
```bash
python3 main.py /dev/ttyACM0``
```