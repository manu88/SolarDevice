#!/bin/bash
# ─────────────────────────────
# WARNING WINDOW (LEFT)
# ─────────────────────────────
lxterminal \
--geometry=80x25+0+0 \
-e bash -c '
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo " SOLAR DEVICE WARNING"
echo " the app won t stop when closing the window"
echo " To close it you need to run the command "
echo "sudo systemctl stop solar_device.service"
echo "sudo systemctl stop display-controller.service"
echo "sudo systemctl stop pd.service"
echo "or enter stop inside this console"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo ""
echo "Type: stop → stop service"
echo "Type: exit → close window"
echo ""
while true; do
    read -p "> " cmd

    if [ "$cmd" = "stop" ]; then
        sudo systemctl stop solar_device.service
        sudo systemctl stop display-controller.service
        sudo systemctl stop pd.service

        echo "Service stopped."
        break
    fi

    if [ "$cmd" = "exit" ]; then
        break
    fi
done

exec bash
' &

# ─────────────────────────────
# JOURNAL WINDOW (RIGHT)
# ─────────────────────────────
lxterminal \
--geometry=120x25+0+100 \
-e bash -c '
echo "Loading logs..."
echo ""

journalctl -u solar_device.service --no-pager -n 100

echo ""
echo "--- LIVE LOGS ---"

journalctl -u solar_device.service -f

exec bash
' &
