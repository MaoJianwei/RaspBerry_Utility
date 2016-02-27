sudo amixer cset numid=3 1 &
sudo python -m SimpleHTTPServer 80 &
# sudo python /home/pi/MaoSystem/readDLNA.py &
sudo python /home/pi/MaoSystem/monitor.py &
sudo python /home/pi/MaoSystem/DNS.py &
sudo mount -o uid=pi,gid=pi /dev/sda /home/pi/MaoUdisk # should not put &
/home/pi/MaoSystem/modesmixer2.sh &

