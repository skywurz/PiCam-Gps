# PiCam-Gps
This is a project that allows you to record video with a raspberry pi and in the process capture images and gps coordinants.
It then generates a KML file and uploads it as well as the pictures to your ftp server. 

For an example of what things should looklike if everything is working properly http://skywurz.com/traffic/xje34az.html

The exicutable rpi3-gpiovirtbuf is from
https://github.com/6by9/rpi3-gpiovirtbuf.git

Pi Pre-recs:
sudo apt-get update
sudo apt-get upgrade
sudo raspi-config ### and enable the camera
sudo apt-get install python3-picamera
sudo apt-get install gpsd gpsd-clients python-gps
sudo apt-get install pip3
sudo apt-get install screen
sudo apt-get install mkvtoolnix
sudo pip3 install ephem
sudo pip3 install gps3
sudo apt-get install apache2
sudo a2enmod cgi
sudo a2dismod deflate #makes CGIs load before return
sudo service apache2 restart


Full list of python3 libs:
chardet (2.3.0)
colorama (0.3.2)
decorator (3.4.0)
ephem (3.7.6.0)
gps3 (0.33.3)
html5lib (0.999)
ipython (2.3.0)
numpy (1.8.2)
picamera (1.12)
pip (1.5.6)
psutil (5.0.1)
pycrypto (2.6.1)
requests (2.4.3)
setuptools (5.5.1)
simplegeneric (0.8.1)
six (1.8.0)
urllib3 (1.9.1)
wheel (0.24.0)

