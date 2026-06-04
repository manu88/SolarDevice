#!/bin/bash
sudo rfkill unblock bluetooth
sudo systemctl start bluetooth
sleep 1
bluetoothctl power on
exit 0

