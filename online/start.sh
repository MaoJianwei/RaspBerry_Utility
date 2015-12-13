sudo mount -o uid=pi,gid=pi /dev/sda1 /home/pi/MaoUdisk &
sudo amixer cset numid=3 1 &
sudo python -m SimpleHTTPServer 80 &
sudo python /home/pi/MaoSystem/readDLNA.py &
sudo python /home/pi/MaoSystem/monitor.py &