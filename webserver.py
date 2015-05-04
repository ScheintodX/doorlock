#!/usr/bin/env python3


import html
import traceback
import socket
import ssl
import http.server
import sys
import os
import csv
from urllib.parse import urlparse
from urllib.parse import parse_qs
import random
import qr
import subprocess
import time
import cgi
import auth3

import door

HOST = 'lock.binary.kitchen'
#HOST = '0.0.0.0'
#HOST = '172.23.4.222'
SSL = True
PORT = 443 if SSL else 80

OP = {'box_size': 4, 'pic': '/home/pi/lock/pic.png', 'template': '/home/pi/lock/template.png'}

SECRET = ""

def genRand():

	global SECRET

	SECRET = "%X" % random.getrandbits(64)


def genQr():

	global SECRET

	genRand();

	qr.do( "https://%s:%d?c=%s" % ( HOST, PORT, SECRET ), sys.path[0], OP )

def secret():

	global SECRET

	return SECRET

class BinaryKitchenHTTPRequestHandler( http.server.BaseHTTPRequestHandler ):

	def parse_POST( self ):

		para = dict()

		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],}
		)
		return form


	def send_template( self, theFile, c ):

		self.send_response( 200 )
		self.send_header( 'Content-type', 'text-html' )
		self.end_headers()
	
		data = self.load( "/home/pi/lock/" + theFile )
		data = data.replace( '%c%', "%s" % c )

		self.wfile.write( bytes( data, 'UTF-8' ) )

	# GET: Show login form or some errors
	# when c is missing regenerate qr code
	def do_GET( self ):

		try:

			o = urlparse(self.path)
			para = parse_qs(o.query)

			if "/favicon.ico" in self.path:
				return

			if 'c' not in para:
				self.sendError( "Missing: 'c'. Please login via QR-Code." )
				return

			c = para['c'][0]

			print( "--" )
			print( c )
			print( "--" )
			print( secret() )
			print( "--" )

			if c != secret():
				self.sendError( "Wrong: 'c'" )
				genQr()
				return

			self.send_template( "login.html", c )
			#self.send_response( 200 )
			#self.send_header( 'Content-type', 'text-html' )
			#self.end_headers()
		
			#data = self.load( "login.html" )
			#data = data.replace( '%c%', "%s" % c )

			#self.wfile.write( bytes( data, 'UTF-8' ) )
			
			return
            
		except IOError:
			self.send_error(404, 'file not found')


	# POST: Unlock door if secret(c), user(u) and pass(p) match
	def do_POST(self):

		try:
		
			form = self.parse_POST()

			print( form )
		
			if "c" not in form or "u" not in form or "p" not in form or "action" not in form:

				self.sendError( "Missing parameters: any of 'c', 'p', 'u'" )
				return

			c = form.getvalue( "c" )

			if c != secret():

				self.sendError( "Wrong parameter: 'c'" );
				return;

			if not auth3.auth( form.getvalue("u"), form.getvalue("p") ):

				self.sendError( "Not allowed" );
				return;

			action = form.getvalue('action')

			if action == 'open':
				door.unlock()
				door.open()

			elif action == 'lock':
				door.lock()

			#self.send_header( 'Location', '/' )
			self.send_template( "success.html", "" )

			genQr()

		except IOError:
			self.send_error( 404, 'file not found' )


	def load( self, filename ):

		with open( filename ) as content:
			return content.read()
		

	def sendError( self, message ):

		data = self.load( "error.html" )
		data = data.replace( '%message%', message )

		self.send_error( 400, message )
		self.wfile.write( bytes( data, 'UTF-8') )


def serve(): 
			
	httpd = http.server.HTTPServer(
			( HOST, PORT ),
			BinaryKitchenHTTPRequestHandler )

	httpd.socket = ssl.wrap_socket( 
			httpd.socket,
			server_side=True,
			certfile='/home/pi/lock/localhost.pem',
			ssl_version=ssl.PROTOCOL_TLSv1 )

	print( "serving..." )
	httpd.serve_forever()

qr.init()

print( "a" )
genQr()

print( "b" )
serve()
print( "c" )

