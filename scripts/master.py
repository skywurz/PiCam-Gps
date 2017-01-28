#!/usr/bin/env python
from gps3 import gps3
from time import *
import ephem
import datetime
import os
import ftplib
import time
import glob
import signal
import threading
from threading import Thread
import psutil
import os.path
import pickle
import subprocess
import picamera
import collections
import shutil
from settings import *

#Some OS level notes
# cgps -s #to look at output
# sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock #to initialize 
# sudo systemctl stop gpsd.socket #to kill gpsd socket 

ftp_cleanup = time.time() - 7*86400 # seven days
safetoshutdown = True
recordinprogress = False
sunup = True
pweroffinten = False
ftperror = False
ftpqueue = []
stillframename = "sad-camera"
lediostat = 0
camhealth = 0
gpsresetloopcount = 0
gpslooptime = datetime.datetime.now()
CONVERSION = {'imperial': (2.2369363, 3.2808399, 'mph', 'feet')}
units = 'imperial'
FTPDir = collections.namedtuple("FTPDir", "name size mtime tree")
FTPFile = collections.namedtuple("FTPFile", "name size mtime")
os.chdir("/home/pi")
########Make PID file ##########
pid = str(os.getpid())
pidfile = scriptpath+"/kmlgps.pid"
if os.path.isfile(pidfile):
    sys.exit()
pidfilew = open(pidfile, 'w')
pidfilew.write(pid)
pidfilew.close()


def timenow():
    global timeString
    global filetimeString
    localtime   = time.localtime()
    timeString  = time.strftime("%I:%M:%S %p - %m/%d/%y", localtime)
    filetimeString  = time.strftime("%Y%m%d_%H%M", localtime)
def unit_conversion(thing, units, length=False):
    """converts base data between metric, imperial, or nautical units"""
    if 'n/a' == thing:
        return 'n/a'
    try:
        thing = round(thing * CONVERSION[units][0 + length], 2)
    except TypeError:
        thing = 'fubar'
    return thing, CONVERSION[units][2 + length]
class FTPDirectory(object):
        def __init__(self, path='.'):
            self.dirs= []
            self.files= []
            self.path= path

        def getdata(self, ftpobj):
            ftpobj.retrlines('MLSD', self.addline)

        def addline(self, line):
            data, _, name= line.partition('; ')
            fields= data.split(';')
            for field in fields:
                field_name, _, field_value= field.partition('=')
                if field_name == 'type':
                    target= self.dirs if field_value == 'dir' else self.files
                elif field_name in ('sizd', 'size'):
                    size= int(field_value)
                elif field_name == 'modify':
                    mtime= time.mktime(time.strptime(field_value, "%Y%m%d%H%M%S"))
            if target is self.files:
                target.append(FTPFile(name, size, mtime))
            else:
                target.append(FTPDir(name, size, mtime, self.__class__(os.path.join(self.path, name))))

        def walk(self):
            for ftpfile in self.files:
                yield self.path, ftpfile
            for ftpdir in self.dirs:
                for path, ftpfile in ftpdir.tree.walk():
                    yield path, ftpfile
try:
    def ftpsender():
        if ftp:
            try:
                ftperror = False
                if ftpqueue != []:
                    session = ftplib.FTP(ftpserveradder,ftpuser,ftppass)
                    for file in ftpqueue:
                        if '.kml' in file:
                            file = open(file,'rb')  # file to send      
                            session.cwd('/')
                            session.storbinary('STOR bikekml.kml', file)     # send the file
                            file.close()                                    # close file
                            ftpqueue.remove(file)
                        else:
                            if '.jpg' in file:
                                session.cwd('/')
                                filename = file.replace(localstore , 'STOR ')
                                filename = filename.replace('/' , '')
                                file = open(file,'rb')  # file to send  
                                session.cwd('img')
                                session.storbinary(filename, file)     # send the file
                                file.close()
                                ftpqueue.remove(file)
                                session.cwd('/')                            
                    session.quit()
                ftpcleanup()
                time.sleep(30)
            except:
                ftperror = True
                print('FTP Error')
    ####Cleans up old files on ftp server####    
    def ftpcleanup():
        if ftp:
            try:
                session = ftplib.FTP(ftpserveradder,ftpuser,ftppass)
                session.cwd('img') # if it's '.', you can skip this line
                folder = FTPDirectory()
                folder.getdata(session) # get the filenames
                for path, ftpfile in folder.walk():
                    if ftpfile.mtime < ftp_cleanup:
                        if ftpfile.name != '.' and ftpfile.name != '..':
                            session.delete(ftpfile.name)
                            print(ftpfile.name + " Removed From FTP")
                session.quit()
            except:
                pass
                
    ######Sat Counter#######            
    def satellites_used(feed):
    ###Counts number of satellites used in calculation from total visible satellites

        total_satellites = 0
        used_satellites = 0

        if not isinstance(feed, list):
            return 0, 0

        for satellites in feed:
            total_satellites += 1
            if satellites['used'] is True:
                used_satellites += 1
        return total_satellites, used_satellites
    ########Get WIFI SSIDS##########
    def wifissids(): 
        global home
        global mobile
        global work
        ssids = os.popen('sudo iwlist wlan0 scan | grep ESSID')
        preprocessed = ssids.read()
        ssids.close()
        preprocessed = preprocessed.split('\n')
        preprocessed = [w.replace('ESSID:"', '') for w in preprocessed]
        preprocessed = [w.replace('"', '') for w in preprocessed]
        preprocessed = [w.replace(' ', '') for w in preprocessed]
########Found SSIDS   
        home = homessid in preprocessed  
        mobile = mobilessid in preprocessed  
        work = workssid in preprocessed  
        home_mobile = all(x in preprocessed for x in [homessid, mobilessid])    
        work = all(x in preprocessed for x in [workssid, mobilessid])

                
    ########Get Up Time##########
    def uptime():
        global uptimetxt
        uptimesec = os.popen("awk '{print $1}' /proc/uptime").readline()
        m, s = divmod(float(uptimesec), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        uptimetxt = "%02d:%02d:%02d:%02d" % (d, h, m, s)
        uptimestr = "System Uptime:"+uptimetxt
        return uptimestr

    ########Get Free Space on SD Card##########
    def freespace():
        size = os.statvfs(usbcardpath)
        size = (size.f_bavail * size.f_frsize)
        sizemb = size/1024/1024
        def sizeof_fmt(num, suffix='B'):
            for unit in ['','K','M','G','T','P','E','Z']:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num, unit, suffix)
                num /= 1024.0
            return "%.1f%s%s" % (num, 'Yi', suffix)
        freespace = sizeof_fmt(size)
        return sizemb
        
    ########Get Free Space on Local Disk##########
    def localfreespace():
        size = os.statvfs(localstore)
        size = (size.f_bavail * size.f_frsize)
        sizemb = size/1024/1024
        def sizeof_fmt(num, suffix='B'):
            for unit in ['','K','M','G','T','P','E','Z']:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num, unit, suffix)
                num /= 1024.0
            return "%.1f%s%s" % (num, 'Yi', suffix)
        freespace = sizeof_fmt(size)
        return sizemb        

    ########Get Oldest File##########
    def purge():
        files = sorted(glob.iglob(usbcardpath+'/*'), key=os.path.getctime)
        if files != []:

            fcnt = len(files) - 1
            oldest = files[0]
            if os.path.isdir(oldest) and fcnt >= 1:               
                lcnt = 1
                while os.path.isdir(oldest):
                    oldest = files[lcnt]
                    lcnt += 1
                    if lcnt >= fcnt:
                        break
            newest = files[-1]
            sizemb = freespace()
            ###########Delete Oldest File If less than x ammount of disk space##########
            if sizemb <= 6144:
                if not os.path.isdir(oldest):
                    os.remove(oldest)
                
    ########Get Oldest File on local disk##########
    def localpurge():
        files = sorted(glob.iglob(localstore+'/*'), key=os.path.getctime)
        if files != []:
            fcnt = len(files) - 1
            oldest = files[0]
            if os.path.isdir(oldest) and fcnt >= 1:               
                lcnt = 1
                while os.path.isdir(oldest):
                    oldest = files[lcnt]
                    lcnt += 1
                    if lcnt >= fcnt:
                        break
                    
            newest = files[-1]
            sizemb = freespace()
            ###########Delete Oldest File If less than x ammount of disk space##########
            if sizemb <= 512:
                if not os.path.isdir(oldest):
                    os.remove(oldest)
                    
    ########Keep Only 6 files in web dir##########
    def webpurge():
        files = sorted(glob.iglob('/var/www/html/img/*'), key=os.path.getctime)
        if files != []:
            fcnt = len(files) - 1
            oldest = files[0]
            if os.path.isdir(oldest) and fcnt >= 1:               
                lcnt = 1
                while os.path.isdir(oldest):
                    oldest = files[lcnt]
                    lcnt += 1
                    if lcnt >= fcnt:
                        break
                    
            newest = files[-1]
            sizemb = freespace()
            ###########Delete Oldest File If less than x ammount of disk space##########
            if fcnt >= 5:
                if not os.path.isdir(oldest):
                    os.remove(oldest)
    
    ##########Move Local To USB Archive#####
    def archive():
        safetoshutdown = False
        files = sorted(glob.iglob(localstore+'/*'), key=os.path.getctime)
        for stuff in files:
            try:
                if "h264" in stuff:
                    filenames = stuff.replace(localstore, usbcardpath)
                    filenames = filenames.replace("h264", "mkv")
                    #convert = subprocess.check_output('avconv -i '+ stuff + ' -codec copy -c copy -y '+ filenames +' ;exit 0', shell=True)
                    convert = subprocess.check_output('mkvmerge --output '+filenames+' --language 0:und --default-duration 0:49fps '+stuff +' ;exit 0', shell=True)
                    os.remove(stuff)
                else:
                    shutil.move(stuff, usbcardpath+'/')
            except:
                if "h264" in stuff:
                    filenames = stuff.replace(localstore, usbcardpath)
                    filenames = filenames.replace("h264", "mkv")
                    os.remove(filenames)
                    shutil.move(stuff, usbcardpath+'/')
                else:
                    filenames = stuff.replace(localstore, usbcardpath)
                    os.remove(filenames)
                    shutil.move(stuff, usbcardpath+'/')
        else:
            safetoshutdown = True
            print("archive script finished")
    
    ########Get Sunrise Sunset ###########
    def sunstatus():
        global sunup
        now_timestamp = time.time()
        offset = datetime.datetime.now() - datetime.datetime.utcnow()
        #Make an observer
        yourhere = ephem.Observer()
        now_date = time.strftime("%Y/%m/%d")
        #PyEphem takes and returns only UTC times.
        yourhere.date = now_date + " 15:00:00"

        #Location
        yourhere.lon  = str(long) #Note that lon should be in string format
        yourhere.lat  = str(lat)      #Note that lat should be in string format

        #Elevation in metres
        yourhere.elev = 20

        #To get U.S. Naval Astronomical Almanac values, use these settings
        yourhere.pressure= 0
        yourhere.horizon = '-0:34'

        sunrise=yourhere.previous_rising(ephem.Sun()) #Sunrise
        sunrise = sunrise.datetime() + offset
        noon   =yourhere.next_transit   (ephem.Sun(), start=sunrise) #Solar noon
        noon = noon.datetime() + offset
        sunset = yourhere.next_setting   (ephem.Sun()) #Sunset
        sunset = sunset.datetime() + offset
        print(sunset)
        fifteendatetimemin = datetime.timedelta(minutes=15)
        presunset = sunset - fifteendatetimemin
        postsunrise = sunrise + fifteendatetimemin
        if presunset <= datetime.datetime.now() or postsunrise >= datetime.datetime.now(): 
            sunup = False
        else:
            sunup = True
            
    ######Changes LED State######        
    def ledstate():
        global lediostat
        if sunup:
            led = subprocess.Popen(['scripts/./rpi3-gpiovirtbuf', 's', '134', '0'])
            lediostat = 0
        else:
            led = subprocess.Popen(['scripts/./rpi3-gpiovirtbuf', 's', '134', '1']) 
            lediostat = 1            
            
    ######## Get Camera Connection Status######
    def camerastat():
        if camhealth == 1:
            connectedcam = True
            return connectedcam
        else:
            connectedcam = False
            return connectedcam
    ######## GPS Service Reset#######
    def gpsreset():
        devs = sorted(glob.iglob('/dev/*'))
        cnt = 0
        for d in devs:
            usb = '/dev/ttyUSB'+str(cnt)
            if usb in devs:
                servinit = subprocess.Popen(['sudo','systemctl','stop','gpsd.socket'])
                servinit = subprocess.Popen(['sudo','gpsd','/dev/'+usb,'-F','/var/run/gpsd.sock'])
                print('Found GPS Socket ' + usb)
                break
            else:
                cnt += 1
            
        
    ########GPS KML##########
    def gpskml():
        print('GPS Thread Starting')
        while gps:
            #servinit = subprocess.Popen(['sudo','systemctl','stop','gpsd.socket'])
            #servinit = subprocess.Popen(['sudo','gpsd','/dev/ttyUSB0','-F','/var/run/gpsd.sock'])
            gpsreset()
            global lat
            global long
            global gpslooptime
            global gpsresetloopcount
            
            gpslooptime = datetime.datetime.now()
            time.sleep(10)
            ###########Get GPS Data##############    
            gpsd_socket = gps3.GPSDSocket()
            gpsd_socket.connect(host='127.0.0.1', port=2947)
            gpsd_socket.watch()
            data_stream = gps3.DataStream()
        
            lat = 0.0
            while lat == 0.0:
                for new_data in gpsd_socket:
                    if new_data:
                        data_stream.unpack(new_data)
                    fivedatetimemin = datetime.timedelta(minutes=2)
                    gpslooptimeplus = gpslooptime + fivedatetimemin
                    #Check For Indefinate loop of no data
                    if  gpslooptimeplus <= datetime.datetime.now():
                        servinit = os.popen('sudo sh -c "echo 0 > /sys/bus/usb/devices/1-1.3/authorized"')
                        servinit = os.popen('sudo sh -c "echo 1 > /sys/bus/usb/devices/1-1.3/authorized"')
                        gpsthread.isAlive()
                        deadgps()
                        gpsresetloopcount += 1
                        print('GPS has been reset '+str(gpsresetloopcount)+' times')
                        if gpsresetloopcount >= 15:
                            os.system("reboot now")
                        raise Exception('No GPS Fix For over 2 min killing thread!')    
                    if data_stream.TPV['lat'] != 'n/a':
                        speed = data_stream.TPV['speed']
                        lat = data_stream.TPV['lat']
                        long = data_stream.TPV['lon']
                        print(lat)
                        speed = ('Speed:{} {}'.format(*unit_conversion(data_stream.TPV['speed'], units)))
                        altitude = ('Altitude:{} {}'.format(*unit_conversion(data_stream.TPV['alt'], units, length=True)))
                        gpsstatus = ('Status:{:<}D  '.format(data_stream.TPV['mode']))
                        laterr = ('Latitude Err:+/-{} {}'.format(*unit_conversion(data_stream.TPV['epx'], units, length=True)))
                        longerr = ('Longitude Err:+/-{} {}'.format(*unit_conversion(data_stream.TPV['epy'], units, length=True)))
                        alterr = ('Altitude Err:+/-{} {}'.format(*unit_conversion(data_stream.TPV['epv'], units, length=True)))
                        speederr = ('Speed Err:+/-{} {}'.format(*unit_conversion(data_stream.TPV['eps'], units)))
                        satsused = ('Using {0[1]}/{0[0]} satellites (truncated)'.format(satellites_used(data_stream.SKY['satellites'])))
                        break



            sunstatus()
            gpsresetloopcount = 0
            if recordenable:
                photo()
            localtime   = time.localtime()
            timeString  = time.strftime("%I:%M:%S %p - %m/%d/%y", localtime)
            sysuptime = uptime()
            #######Append GPS File##########
            try:
                gpshistr = open(scriptpath+'/'+'gpshist.txt', 'r')
            except:
                gpshistr = open(scriptpath+'/'+'gpshist.txt', 'w')
                gpshistr.close()
                gpshistr = open(scriptpath+'/'+'gpshist.txt', 'r')
            #######try to open pickle file##########
            try:
                gpshistrpyl = open(scriptpath+'/'+'gpshist.pyl', 'rb')
                gpspyl = pickle.load(gpshistrpyl)
                gpshistrpyl.close()
            except:
                gpspyl = {}
                gpshistrpyl = open(scriptpath+'/'+'gpshist.pyl', 'wb')
                pickle.dump(gpspyl,gpshistrpyl)
                gpshistrpyl.close()
            #original_gps = gpshistr.read()
            gpspreprocessed = gpshistr.read()
            
            gpshistr.close()
            
            gpspreprocessed = gpspreprocessed.split('\n')
            gpspreprocessed.insert(0, str(long) + ','+ str(lat))
            gpspreprocessed = list(filter(None, gpspreprocessed))
            htmlbr = "<br />"

            gpsdiscrip = '<![CDATA[<a href="img/'+stillframename+'.jpg" target="_blank">'+'<img src="img/'+stillframename+'.jpg"'+"style="+"width:320px;height:180px;"+"/></a>]]>"+htmlbr+str(gpsstatus)+htmlbr+str(speed)+htmlbr+str(speederr)+htmlbr+str(altitude)+htmlbr+str(alterr)+htmlbr+str(laterr)+htmlbr+str(longerr)+htmlbr+satsused+htmlbr+str(sysuptime)+htmlbr

            gpshistsize = len(gpspreprocessed)
            gpspylsize = len(gpspyl)
            gpspylcnt = gpspylsize
            gpspylnew = {}
            gpspylnew[0] = timeString,str(long) + ','+ str(lat),str(gpsdiscrip)

            if gpspylsize == 1:
                gpspylnew[1] = gpspyl[0]
            else:
                for keys in gpspyl:
                    gpspylnew[(keys + 1)] = gpspyl[keys]
                    if keys == 47:
                        break
            
            gpshistrpyl = open(scriptpath+'/'+'gpshist.pyl', 'wb')
            pickle.dump(gpspylnew,gpshistrpyl)
            gpshistrpyl.close()
            #print(gpspylnew.items())
            gpshistw = open(scriptpath+'/'+'gpshist.txt', 'w')
            bikekml = open(scriptpath+'/'+'bikekml.kml', 'w')

            ##Bike KML header
            bikekml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            bikekml.write("<kml xmlns=\"http://earth.google.com/kml/2.2\">\n")
            bikekml.write("<Document>\n")
            bikekml.write('<Style id="lastPlacemark">'+"\n")
            bikekml.write("<IconStyle>\n")
            bikekml.write("<Icon>\n")
            bikekml.write("<href>http://maps.google.com/mapfiles/kml/shapes/motorcycling.png</href>\n")
            bikekml.write("</Icon>\n")
            bikekml.write("</IconStyle>\n")
            bikekml.write("</Style>\n")
            bikekml.write('<Style id="oldPlacemark">'+"\n")
            bikekml.write("<IconStyle>\n")
            bikekml.write("<Icon>\n")
            bikekml.write("<href>http://maps.google.com/mapfiles/kml/paddle/red-circle-lv.png</href>\n")
            bikekml.write("</Icon>\n")
            bikekml.write("</IconStyle>\n")
            bikekml.write("</Style>\n")
            


            for keys in gpspylnew:
                gpscoor = gpspylnew[keys]
                gpshistw.write(gpscoor[1] + "\n")
                ###Bike KML Body
                if keys == 0:
                    bikekml.write("<Placemark>\n")
                    bikekml.write("<name>"+ gpscoor[0] +"</name>\n")
                    bikekml.write("<description>"+ gpscoor[2]+"</description>\n")
                    bikekml.write("<styleUrl>#lastPlacemark</styleUrl>\n")
                    bikekml.write("<Point>\n")
                    bikekml.write("<coordinates>\n")
                    bikekml.write(gpscoor[1] + ",0\n")
                    bikekml.write("</coordinates>\n")
                    bikekml.write("</Point>\n")
                    bikekml.write("</Placemark>\n")
                else:
                    bikekml.write("<Placemark>\n")
                    bikekml.write("<name>"+ gpscoor[0] +"</name>\n")
                    bikekml.write("<description>"+ gpscoor[2] +"</description>\n")
                    bikekml.write("<styleUrl>#oldPlacemark</styleUrl>\n")
                    bikekml.write("<Point>\n")
                    bikekml.write("<coordinates>\n")
                    bikekml.write(gpscoor[1] + ",0\n")
                    bikekml.write("</coordinates>\n")
                    bikekml.write("</Point>\n")
                    bikekml.write("</Placemark>\n")
                #print gpscoor
            gpshistw.close()
            ###Bike KML Foot
            bikekml.write("</Document>\n")
            bikekml.write("</kml>\n")            
            bikekml.close()
                             ######FTP Queue#########
            if ftp:
                ftpqueue.append(scriptpath+'/'+'bikekml.kml')      
                if recordenable:
                    ftpqueue.append(localstore+'/'+stillframename+'.jpg')
                    
            time.sleep(140)
    #####Takes Photo From Running Video####        
    def photo():
        global stillframename
        if camerastat():
            try:
                if recordinprogress:
                    stillframename = filetimeString
                    camera.capture(localstore+'/'+stillframename+'.jpg', use_video_port=True)
                else:
                    time.sleep(5)
                    if recordinprogress:
                        stillframename = filetimeString
                        camera.capture(localstore+'/'+stillframename+'.jpg', use_video_port=True)
            except:
                stillframename = filetimeString
                shutil.copy(scriptpath+'/sad-camera.jpg',localstore+'/'+stillframename+'.jpg') 
        else:
            stillframename = filetimeString
            shutil.copy(scriptpath+'/sad-camera.jpg',localstore+'/'+stillframename+'.jpg') 
    ########Uploads an image if GPS is Not working#######
    def deadgps():
            if recordenable:
                photo()
                htmlbr = "<br />"
                bikekml = open(scriptpath+'/'+'bikekml.kml', 'w')
                gpsdiscrip = timeString+htmlbr+'<![CDATA[<a href="img/'+stillframename+'.jpg" target="_blank">'+'<img src="img/'+stillframename+'.jpg"'+"style="+"width:320px;height:180px;"+"/></a>]]>"
                ##Bike KML header
                bikekml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                bikekml.write("<kml xmlns=\"http://earth.google.com/kml/2.2\">\n")
                bikekml.write("<Document>\n")
                bikekml.write('<Style id="lastPlacemark">'+"\n")
                bikekml.write("<IconStyle>\n")
                bikekml.write("<Icon>\n")
                bikekml.write("<href>http://maps.google.com/mapfiles/kml/shapes/info_circle.png</href>\n")
                bikekml.write("</Icon>\n")
                bikekml.write("</IconStyle>\n")
                bikekml.write("</Style>\n")
                bikekml.write('<Style id="oldPlacemark">'+"\n")
                bikekml.write("<IconStyle>\n")
                bikekml.write("<Icon>\n")
                bikekml.write("<href>http://maps.google.com/mapfiles/kml/paddle/red-circle-lv.png</href>\n")
                bikekml.write("</Icon>\n")
                bikekml.write("</IconStyle>\n")
                bikekml.write("</Style>\n")
                bikekml.write("<Placemark>\n")
                bikekml.write("<name>"+ '"GPS Data is Unavalible"' +"</name>\n")
                bikekml.write("<description>"+ gpsdiscrip +"</description>\n")
                bikekml.write("<styleUrl>#lastPlacemark</styleUrl>\n")
                bikekml.write("<Point>\n")
                bikekml.write("<coordinates>\n")
                bikekml.write("-122.0081025,38.2537101,0\n")
                bikekml.write("</coordinates>\n")
                bikekml.write("</Point>\n")
                bikekml.write("</Placemark>\n")
                ###Bike KML Foot
                bikekml.write("</Document>\n")
                bikekml.write("</kml>\n")            
                bikekml.close()
                                 ######FTP Queue#########
                if ftp:
                    ftpqueue.append(scriptpath+'/'+'bikekml.kml')
                    if recordenable:
                        ftpqueue.append(localstore+'/'+stillframename+'.jpg')

   
    ########Record Video###########
    def recorder():
        print('Recorder Thread Starting')
        while record:
            safetoshutdown = False
            global recordinprogress
            global camera
            global camhealth
            try:
                camera = picamera.PiCamera()
                camera.resolution = (1280, 720)
                camera.framerate = 49
                camhealth = 1
            except:
                camhealth = 0
                print("Camera Not Detected")
                raise Exception('No Camera Detected killing thread!')
            camera.start_recording(localstore+'/'+filetimeString+'.h264')
            ledstate()
            recordinprogress = True
            camera.wait_recording(150)
            if not record:
                camera.stop_recording()
                recordinprogress = False
                camera.close()
            else:
                ledstate()
                camera.wait_recording(150)
                if not record:
                    camera.stop_recording()
                    recordinprogress = False
                    camera.close()
                else:
                    ledstate()
                    camera.wait_recording(150)
                    if not record:
                        camera.stop_recording()
                        recordinprogress = False
                        camera.close()
                    else:
                        ledstate()
                        camera.wait_recording(150)
                        camera.stop_recording()
                        recordinprogress = False
                        camera.close()

    ########Make Stats File###########
    def statsexport():
    #######try to open pickle file##########

        ststspkl = {}
        statsexportpkl = open(scriptpath+'/'+'ststspkl.pyl', 'wb')
        #Last update
        ststspkl[0] = timeString
        #Last Photo
        webpurge()
        try:
            shutil.copy(localstore+'/'+stillframename+'.jpg','/var/www/html/img/'+stillframename+'.jpg',) 
        except:
            shutil.copy(scriptpath +'/'+stillframename+'.jpg','/var/www/html/img/'+stillframename+'.jpg',) 
        ststspkl[1] = stillframename+'.jpg'
        #GPS Status
        ststspkl[2] = gpsenable
        ststspkl[3] = gps
        ststspkl[4] = gpsresetloopcount
        #Camera Status
        ststspkl[5] = recordenable
        ststspkl[6] = record
        ststspkl[7] = lediostat
        ststspkl[12] = camerastat()
        #FTP Status
        ststspkl[8] = ftp
        ststspkl[13] = ftperror
        #System Status
        ststspkl[9] = gpslooptime
        ststspkl[10] = safetoshutdown
        ststspkl[11] = pweroffinten
        pickle.dump(ststspkl,statsexportpkl)
        statsexportpkl.close()

    
    
    ########Threads########
    gpsthread = threading.Thread(target=gpskml)
    #add recorder thread add dates to recorder files  
    recordthread = threading.Thread(target=recorder)
    #add ftp move thread
    ftpthread = threading.Thread(target=ftpsender)
    #########Main Loop#######################        
    while True:
        wifissids()        
        while mobile or testing:
            purge()
            localpurge()
            wifissids()
            timenow()
            wifissids()

            
            if gpsenable:
                gps = True
                if not gpsthread.isAlive():
                    gpsthread._stop()
                    gpsthread = threading.Thread(target=gpskml)
                    gpsthread.start()  
            if recordenable:
                record = True
                if not recordthread.isAlive():
                    recordthread._stop()
                    recordthread = threading.Thread(target=recorder)
                    recordthread.start()
            if ftp:
                if not ftpthread.isAlive():
                    ftpthread._stop()
                    ftpthread = threading.Thread(target=ftpsender)
                    ftpthread.start()            
            statsexport()        
            time.sleep(30)
        else:
            wifissids()
            timenow()
            purge()
            if not recordinprogress:
                archive()
                try:
                    os.remove(scriptpath+'/'+'gpshist.pyl')
                    print('removed gpshist.pyl')
                except:
                    pass
            gps = False
            record = False
            hourofday = datetime.datetime.now().time()
            autoshutdowntime = datetime.time(19) 
            if safetoshutdown and hourofday >= autoshutdowntime and home and not testing and not mobile:
                print(uptime())
                if uptimetxt > "00:00:10:00":
                    print("System will Powered off in 10 Min")
                    time.sleep(600)
                    pweroffinten = True
                    os.system("poweroff")
            statsexport()        
            time.sleep(30)
            
        time.sleep(30)

        
finally:
    os.unlink(pidfile) 
    pass
    
