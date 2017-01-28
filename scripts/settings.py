# settings.py

####################Globals##########################

####Folder Paths###
usbcardpath = "usbstore"
localstore = "localstore"
scriptpath = "scripts"

####Enable Components####
ftpenabled = True
gpsenable = True
recordenable = True
testing = False

####SSIDs####
homessid = 'HomeWifi'
mobilessid = 'MobilWiFi'
#mobilessid = 'test'
workssid = 'WorkWiFi'

####FTP Credentials####
ftpserveradder = 'ftp.yourwebsite.com'
ftpuser = 'user@yourwebsite.com'
ftppass = 'pass'

####GPS Settings####
gpslooptime = 140 #How often the gps updates location (and photo)subtract 10 sec
gpsmappoints = 47 #Number of points to keep before overwriting them
gpsnonfixreset = 15 #Number of times the gps will break out of timeout before it resets the whole system. Hint: gpsnonfixreset*gpstimeouttime = how long befor systemreset in Min
gpstimeouttime = 1 #The ammount of time IN MINUNETS the system waits for gps fix before resetting the gps USB port and killing gps thread
