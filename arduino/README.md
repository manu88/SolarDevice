# détails des fichiers

- 'comLeds' : contrôle des LEDS depuis le patch pd control2.pd
- 'testLeds' : contrôle des LEDS automatique (mode ON/OFF/Blink),sans pd et depuis la console d'arduino. Contient le code refactoré du compte-tours
- 'revCount' : précédement code du compte tour

# Protocole pd->arduino

## adressage leds

message de 3 octets contenant:
`[byte]0X17 [byte]led-id[0-255] [byte]intensity[[0-255]]`

# Protocole arduino->pd

Utilise le format `fudi` (fast universal digital interface), qui est simple à lire dans pd.
