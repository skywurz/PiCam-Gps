#!/usr/bin/python3
import cgi
import os
import time
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
	<body>''')
    print('<div class="featuresg">')
print('<article>')
<i class="icon fa-refresh fa-spin fa-3x fa-fw"></i>
<span class="sr-only">Loading...</span>
print(''' <div class="content">
<h3>GPS</h3>
<!-- <p>GPS Connectivity and </p> -->
</div>
</div>
</article>''')
os.system("reboot now")

