#!/bin/bash

echo "🔧 Refuerzo para sistema con overlay activado..."

# 1. Desactivar swap
echo "➡️  Desactivando swap..."
sudo swapoff -a
sudo systemctl disable dphys-swapfile
sudo rm -f /var/swap
sudo sed -i 's/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=0/' /etc/dphys-swapfile

# 2. Desactivar servicios de logs persistentes
echo "➡️  Desactivando servicios de log persistentes..."
sudo systemctl disable rsyslog
sudo systemctl disable logrotate
sudo systemctl disable man-db.timer
sudo systemctl disable apt-daily.timer
sudo systemctl disable apt-daily-upgrade.timer

# 3. Montar /var/log en RAM
echo "➡️  Montando /var/log como tmpfs..."

# Agrega entrada solo si no existe
if ! grep -q "^tmpfs\s\+/var/log" /etc/fstab; then
  echo "tmpfs   /var/log  tmpfs  defaults,noatime,nosuid,size=64m  0  0" | sudo tee -a /etc/fstab
fi

echo "✅ Listo. Reinicia la Raspberry Pi para aplicar los cambios."

