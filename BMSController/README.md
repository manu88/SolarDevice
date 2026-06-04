# daemon de communication avec la batterie AllPowers R1500 Lite

Code original: [https://github.com/jolle22/allpowers-threshold-warner]

## installation

```bash
python3 -m pip install -r requirements.txt --break-system-packages
```

## Usage

```bash
python3 main.py
```

## Ble sur raspberrypi

executer le script init.sh pour activer le bluetooth

## Note

Il y a un bug dans le module "allpowers-ble" qui n'est pas encore corrigé pour le moment (version 0.0.3).
Pour le corriger, dans le fichier allpowers_ble.py, ligne 264, function `_notification_handler` ajouter:

```
 if len(data) < 15:
            return
```python
