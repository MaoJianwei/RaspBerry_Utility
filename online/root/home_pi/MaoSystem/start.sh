# sudo mount -o uid=pi,gid=pi /dev/sda1 /home/pi/MaoUdisk & # maybe should not put &
sudo amixer cset numid=3 1 &
sudo python -m SimpleHTTPServer 80 &
# sudo python /home/pi/MaoSystem/readDLNA.py &
# sudo python /home/pi/MaoSystem/DNS.py &
sudo python /home/pi/MaoSystem/monitor.py four &
# /home/pi/MaoSystem/modesmixer2.sh &
