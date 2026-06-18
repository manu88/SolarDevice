# Scheduler

Gère la logique globale du système.

## usage

```bash
#important: doit être lancé depuis le répertoire racine du repo, i.e, le répertoire parent.
python3 -m Meteo.main config/config-test.json
# spécifier addresse de destination des messages OSC, 127.0.0.1 par défaut.
python3 -m Meteo.main --addr 192.168.1.2 config/config-test.json
```
