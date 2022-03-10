#!/bin/bash

# $ sudo cp areaferrero.sh /usr/local/bin
# $ sudo chmod +x /usr/local/bin/areaferrero.sh
echo ""
echo "Area Ferrero. Startup."
export TERM=vt100
echo $(set | grep TERM)
echo $(date)
# echo $(top -b -n 1 -p 12345)
#
# journalctl --full --all --no-pager -n 10
#
# sudo kill $(ps aux | grep '[p]ython3' | awk '{print $2}')
#
#
cd /home/pi/AreaFerrero/
python3 /home/pi/AreaFerrero/clear_all.py
while ! ip route | grep -oP 'default via .+ dev eth0'; do
  echo "interface not up, will try again in 1 second";
  sleep 2;
done
echo $(i2cdetect -y 1)
# python3 /home/pi/AreaFerrero/i2c_display_oled.py &
# python3 /home/pi/AreaFerrero/call_rgbled.py
# python3 /home/pi/AreaFerrero/rest_server.py &
# python3 /home/pi/AreaFerrero/get_swipe.py &
# python3 /home/pi/AreaFerrero/get_barcode.py &
python3 /home/pi/AreaFerrero/start.py &
# sudo python3 /home/pi/AreaFerrero/open_rele.py &
# python3 /home/pi/AreaFerrero/rest_server.py &
echo "Area Ferrero. Startup Completed."
# python3 /home/pi/AreaFerrero/get_nfc.py &