# Documentation

## Messages OSC

### Météo

| Adresse        |      Arguments     |     Notes                                  |
|----------------|--------------------|--------------------------------------------|
| `/nebulosity`  | `[float, float]`   | nébulosité actuelle, nébulosité suivante   |
| `/day`         | `int`              |  jour/nuit                                 |

Note: la nébulosité s'exprime entre 0 (pas de nuages) et 1 (temps couvert)

### BMS

| Adresse        |      Arguments     |     Notes                                  |
|----------------|--------------------|--------------------------------------------|
| `/battery`     | `float`            | Pourcentage batterie   |
| `/powerinput`  | `float`            |  puissance en entrée en Watts |
| `/charging`  | `int`            |  en charge sur secteur |

### DisplayController

| Adresse        |      Arguments     |     Notes                                  |
|----------------|--------------------|--------------------------------------------|
| `/sensor`     | `[int, float]`      | capteur i: Vitesse en tour/sec   |

## Câblage Arduino

[![alt](cablageArduinos.png)]
