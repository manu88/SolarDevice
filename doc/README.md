# Documentation

## Configuration

### Configuration des paramètres d'animation de puredata

Simple fichier texte qui se trouve dans le sous-répertoire `Pd`. Pour connaitre le nom du fichier utilisé, voir dans `main.pd`, sous-patch `pd init`, objet `config`.
Ce fichier suit la syntaxe `CLE VALEUR;`

**Attention**: Ne pas oublier les `;` en fin de lignes -- même dans les commentaires!

Si une valeur attendue par puredata n'est pas présente dans le fichier de config, un message `config-search-error: symbol CLE`, où `CLE` est le nom du paramètre de configuration, apparaitra dans la console puredata.

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

## Synopsis logiciels

[![alt](synopsisLogiciel.png)]

## Câblage Arduino

[![alt](cablageArduinos.png)]
