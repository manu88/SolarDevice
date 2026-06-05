# scripts de deployment

## Copier un script dans repertoire systeme
```bash
sudo cp display-controller.service /etc/systemd/system/
```

## Activer au démarrage
```bash
systemctl enable display-controller.service
```

## Checker status
```bash
systemctl status display-controller.service
```

## démarrer service
```bash
systemctl start display-controller.service
```