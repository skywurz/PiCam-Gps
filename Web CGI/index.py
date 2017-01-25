#!/usr/bin/python3
import cgi
import pickle
import os
#featuresg = green
#features = red
#featuresgy= yellow

def uptime():
    uptimesec = os.popen("awk '{print $1}' /proc/uptime").readline()
    m, s = divmod(float(uptimesec), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    uptimetxt = "%02d:%02d:%02d:%02d" % (d, h, m, s)
    uptimestr = "Uptime:<br>"+uptimetxt
    return uptimestr

#######try to open pickle file##########
try:
    statsexportpkl = open('/home/pi/scripts/'+'ststspkl.pyl', 'rb')
    ststspkl = pickle.load(statsexportpkl)
    statsexportpkl.close()
except:
    ststspkl = "err","sad-camera.jpg","err","err","err","err","err","err","err","err","err","err"


#Last update
timeString = ststspkl[0]
#Last Photo
lastphoto = ststspkl[1]
#GPS Status
gpsenable = ststspkl[2]
gps = ststspkl[3]
gpsresetloopcount = ststspkl[4]
#Camera Status
recordenable = ststspkl[5]
record = ststspkl[6]
lediostat = ststspkl[7]
#FTP Status
ftp = ststspkl[8]
#System Status
gpslooptime = ststspkl[9]
safetoshutdown = ststspkl[10]
pweroffinten = ststspkl[11]

   

print("Content-type: text/html \n\n")
print(''' 
<html>
    <head>
        <title>Rasp-Cam</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <!--[if lte IE 8]><script src="../assets/js/ie/html5shiv.js"></script><![endif]-->
        <link rel="stylesheet" href="../assets/css/main.css" />
        <!--[if lte IE 9]><link rel="stylesheet" href="../assets/css/ie9.css" /><![endif]-->
        <!--[if lte IE 8]><link rel="stylesheet" href="../assets/css/ie8.css" /><![endif]-->
    </head>
    <body>

        <!-- Wrapper -->
            <div id="wrapper">

                <!-- Main -->
                    <div id="main">
                        <div class="inner">

                            <!-- Header -->
                                <header id="header">
                                    <a href="index.html" class="logo"><strong>Rasp-Cam</strong></a>
                                    ''')
print('<h3>Last Update: '+timeString+'</h3>')
print('<h3>'+uptime()+'</h3>')
print(''' </header>

                            <!-- Banner -->
                                <section id="banner">
                                    <div class="content">

                                        <ul class="actions">
                                        <li><form name="photo" action="/cgi-bin/photo.py" method="get">
                                        <input class="button big" type="submit" value="Take Photo">
                                        </form></li><br>
                                        
                                        <li><form name="reboot" action="/cgi-bin/reboot.py" method="get">
                                        <input class="button small" type="submit" value="Reboot">
                                        </form><br>
					
                                        <form name="shutdown" action="/cgi-bin/shutdown.py" method="get">
                                        <input class="button small" type="submit" value="Shutdown">
                                        </form></li>
                                        </ul>
                                    </div>
                                    
                                    <span class="image object">''')
                                    
print('<img src="../img/'+ lastphoto +'" alt="" />')
print(''' 
                                    </span>
                                </section>

                            <!-- Section -->
                                <section>
                                    <header class="major">
                                        <h2>Status</h2>
                                </header>''')
####GPS####    
print(''' <div class="content">
<h3>GPS</h3>''')


if gpsresetloopcount > 0:
    print('<p>GPS has looped '+ gpsresetloopcount +' times without a fix</p>')
    print('<div class="featuresy">')
    print('<span class="icon fa-exclamation-triangle"></span>')
    
else:
    if gps:
        print('<div class="featuresg">')
    else:
        print('<div class="features">')
        print('<article>')
        if gpsenable:
        print('<span class="icon fa-check-square"></span>')
        else:
        print('<span class="icon fa-times-circle"></span>')
print('''</div>
</div>
</article>''')
####Camera####
print(''' <div class="content">
<h3>Camera</h3>
<!-- <p>Camera Is connected</p> -->
''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print('''</div>
</div>
</article>''')
####FTP####
print('''<div class="content">
<h3>FTP</h3>
<!-- <p>FTP is running</p> -->
''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print('''</div>
</div>
</article>''')
####System State####
print('''<div class="content">
<h3>System State</h3>
<!--  <p></p> -->
''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print('''</div>
</div>
</article>

<!--  <p></p> -->

							<!-- Section 
								<section>
									<header class="major">
										<h2>Ipsum sed dolor</h2>
									</header>
									<div class="posts">
										<article>
											<a href="#" class="image"><img src="images/pic01.jpg" alt="" /></a>
											<h3>Interdum aenean</h3>
											<p>Aenean ornare velit lacus, ac varius enim lorem ullamcorper dolore. Proin aliquam facilisis ante interdum. Sed nulla amet lorem feugiat tempus aliquam.</p>
											<ul class="actions">
												<li><a href="#" class="button">More</a></li>
											</ul>
										</article>
										<article>
											<a href="#" class="image"><img src="images/pic02.jpg" alt="" /></a>
											<h3>Nulla amet dolore</h3>
											<p>Aenean ornare velit lacus, ac varius enim lorem ullamcorper dolore. Proin aliquam facilisis ante interdum. Sed nulla amet lorem feugiat tempus aliquam.</p>
											<ul class="actions">
												<li><a href="#" class="button">More</a></li>
											</ul>
										</article>
										<article>
											<a href="#" class="image"><img src="images/pic03.jpg" alt="" /></a>
											<h3>Tempus ullamcorper</h3>
											<p>Aenean ornare velit lacus, ac varius enim lorem ullamcorper dolore. Proin aliquam facilisis ante interdum. Sed nulla amet lorem feugiat tempus aliquam.</p>
											<ul class="actions">
												<li><a href="#" class="button">More</a></li>
											</ul>
										</article>
										<article>
											<a href="#" class="image"><img src="images/pic04.jpg" alt="" /></a>
											<h3>Sed etiam facilis</h3>
											<p>Aenean ornare velit lacus, ac varius enim lorem ullamcorper dolore. Proin aliquam facilisis ante interdum. Sed nulla amet lorem feugiat tempus aliquam.</p>
											<ul class="actions">
												<li><a href="#" class="button">More</a></li>
											</ul>
										</article>
										<article>
											<a href="#" class="image"><img src="images/pic05.jpg" alt="" /></a>
											<h3>Feugiat lorem aenean</h3>
											<p>Aenean ornare velit lacus, ac varius enim lorem ullamcorper dolore. Proin aliquam facilisis ante interdum. Sed nulla amet lorem feugiat tempus aliquam.</p>
											<ul class="actions">
												<li><a href="#" class="button">More</a></li>
											</ul>
										</article>
										<article>
											<a href="#" class="image"><img src="images/pic06.jpg" alt="" /></a>
											<h3>Amet varius aliquam</h3>
											<p>Aenean ornare velit lacus, ac varius enim lorem ullamcorper dolore. Proin aliquam facilisis ante interdum. Sed nulla amet lorem feugiat tempus aliquam.</p>
											<ul class="actions">
												<li><a href="#" class="button">More</a></li>
											</ul>
										</article>
									</div>
								</section>

						</div>
					</div>
-->
				<!-- Sidebar -->
					<div id="sidebar">
						<div class="inner">

							<!-- Menu -->
								<nav id="menu">
									<header class="major">
										<h2>Menu</h2>
									</header>
									<ul>
										<li><a href="index.html">Homepage</a></li>
										<li><a href="settings.html">Settings</a></li>
										<li>

						</div>
					</div>

			</div>

		<!-- Scripts -->
			<script src="../assets/js/jquery.min.js"></script>
			<script src="../assets/js/skel.min.js"></script>
			<script src="../assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="../assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="../assets/js/main.js"></script>

	</body>
</html>''')
