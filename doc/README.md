# Documentation

## Configuration

### Configuration des paramètres d'animation de puredata

Simple fichier texte qui se trouve dans le sous-répertoire `Pd`. Par défault il s'agit du fichier `config.txt` Pour connaitre le nom du fichier utilisé, voir dans `main.pd`, sous-patch `pd init`, objet `config`.
Ce fichier suit la syntaxe `CLE VALEUR;`

**Attention**: Ne pas oublier les `;` en fin de lignes -- même dans les commentaires!

Si une valeur attendue par puredata n'est pas présente dans le fichier de config, un message `config-search-error: symbol CLE`, où `CLE` est le nom du paramètre de configuration, apparaitra dans la console puredata.

## Messages OSC

### day-state

exemple pour lever de soleil à 6h et coucher à 22h

| Heure        |      Index     |
|----------------|--------------------|
|    6h-11h            |   0 |
|    11h-13h            |   1 |
|    13h-21h            |   2 |
|    21h-22h            |   3 |
|    22h-6h            |   4 |

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

## Synopsis logiciels

[![alt](synopsisLogiciel.png)]

## Câblage Arduino

[![alt](cablageArduinos.png)]
