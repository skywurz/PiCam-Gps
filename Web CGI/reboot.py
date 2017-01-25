#!/usr/bin/python3 -u
import cgi
import subprocess
import os
import time

print("Content-type: text/html \n\n", flush=True)
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
		<meta http-equiv="refresh" content="3; url=/cgi-bin/index.py" />
	</head>
	<body>
	 <div align="center">
<h3>Rebooting</h3>
<i class="fa fa-refresh fa-spin fa-3x fa-fw"></i>
<span class="sr-only">Loading...</span>
<div class="content">
</article>
</div>
''', flush=True)
time.sleep(5)
os.system('sudo reboot now')
