#!/usr/bin/python3
import cgi
import pickle
#featuresg = green
#features = red
#featuresgy= yellow




print("Content-type: text/html /n/n")
print(''' 
<html>
	<head>
		<title>Rasp-Cam</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<!--[if lte IE 8]><script src="./assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="./assets/css/main.css" />
		<!--[if lte IE 9]><link rel="stylesheet" href="./assets/css/ie9.css" /><![endif]-->
		<!--[if lte IE 8]><link rel="stylesheet" href="./assets/css/ie8.css" /><![endif]-->
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
								<h3>"Last Update:"</h3>
								</header>

							<!-- Banner -->
								<section id="banner">
									<div class="content">

										<ul class="actions">
											<li><a href="#" class="button big" name="Photo">Take Photo</a></li><br>
											<li><a href="#" class="button big" name="Reboot">Reboot</a></li><br>
											<li><a href="#" class="button big" name="Shutdown">Shutdown</a></li><br>
										</ul>
									</div>
									
									<span class="image object">''')
                                    
print('<img src=" images/pic10.jpg " alt="" />')
print(''' 
									</span>
								</section>

							<!-- Section -->
								<section>
									<header class="major">
										<h2>Status</h2>
									</header>''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print(''' <div class="content">
<h3>GPS</h3>
<!-- <p>GPS Connectivity and </p> -->
</div>
</div>
</article>''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print(''' <div class="content">
<h3>Camera</h3>
<!-- <p>Camera Is connected</p> -->
</div>
</div>
</article>''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print('''<div class="content">
<h3>FTP</h3>
<!-- <p>FTP is running</p> -->
</div>
</div>
</article>''')
print('<div class="featuresg">')
print('<article>')
print('<span class="icon fa-check-square"></span>')
print('''<div class="content">
<h3>System State</h3>
<!--  <p></p> -->
</div>
</article>
</div>
</section>

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
			<script src="./assets/js/jquery.min.js"></script>
			<script src="./assets/js/skel.min.js"></script>
			<script src="./assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="./assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="./assets/js/main.js"></script>

	</body>
</html>''')
