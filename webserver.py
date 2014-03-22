#!/usr/bin/env python3

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

HOST = '192.168.0.23'
SSL = True
PORT = 443 if SSL else 80
rannum = random.getrandbits(64)

USER = "koeche"
PASS = "TeusdL"

class BinaryKitchenHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    
	op = {'box_size': 4, 'pic': 'pic.png', 'template': 'template.png'}

	def parse_POST(self):
		para = dict()
		form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
		return form

	#handle GET command
	def do_POST(self):
		try:
			global rannum		
			form = self.parse_POST()
			#print( form )
			#self.log_message( str(o) )
			#send code 200 response
			self.send_response(200)
		
			if "c" not in form or "u" not in form or "p" not in form:
				message = ''.join([
					'<html><body><br>YOU ARE NOT COOKING!!',
					'</body></html>',
					])
				self.send_header('Content-type','text-html')
				self.end_headers()
				self.wfile.write( bytes(message, 'UTF-8') )
				return

			if int(form.getvalue("c")) != rannum:
				message = ''.join([
					'<html><body><br>YOU ARE NOT COOKING!!',
					'</body></html>',
					])

			elif form.getvalue("u") == USER and form.getvalue("p") == PASS:

				relais_process = subprocess.Popen('unlock3s', shell=False, stdin=subprocess.PIPE)
				message = ''.join([
					'<html><body>CLIENT VALUES:<br>',
					'client_address=%s (%s)<br>' % (self.client_address,
												self.address_string()),
					'command=%s<br>' % self.command,
					'path=%s<br>' % self.path,
					'request_version=%s<br>' % self.request_version,
					'',
					'SERVER VALUES:<br>',
					'server_version=%s<br>' % self.server_version,
					'sys_version=%s<br>' % self.sys_version,
					'protocol_version=%s<br>' % self.protocol_version,
					'<br></body></html>',
					])
			else:
				message = ''.join([
					'<html><body><br>YOU ARE NOT COOKING!!',
					'</body></html>',
					])
				
			#send file content to client
			self.send_header('Content-type','text-html')
			self.end_headers()
			self.wfile.write( bytes(message, 'UTF-8') )
			rannum = random.getrandbits(64)
			print( rannum )
			qr.do( "https://%s:%d?c=%d" % ( HOST, PORT, rannum ), sys.path[0], self.op )
			
			return
            
		except IOError:
			self.send_error(404, 'file not found')

	#handle GET command
	def do_GET(self):
		try:
			global rannum		

			o = urlparse(self.path)
			para = parse_qs(o.query)
			#print( para )
			#self.log_message( str(o) )
			#send code 200 response
			self.send_response(200)

			if "/favicon.ico" not in self.path:
				#send header first
				self.send_header('Content-type','text-html')
				self.end_headers()
			
				if "c" not in para:
					message = ''.join([
						'<html><body><br>YOU ARE NOT COOKING!!',
						'</body></html>',
						])
					self.wfile.write( bytes(message, 'UTF-8') )
					return

				if int(para["c"][0]) != rannum:
					message = ''.join([
						'<html><body><br>YOU ARE NOT COOKING!!',
						'</body></html>',
						])

				else:
					if "u" not in para:
						message = ''.join([
							'<html><body><form name="login" method="post">', 
							'User:<input type="text" name="u">',
							'Pass:<input type="password" name="p">',
							'<input type="hidden" name="c" value="%s">' % rannum,
							'<input type="submit" name="login_do_login" value="Login"></form>',
							'</body></html>',
							])
				
						self.wfile.write( bytes(message, 'UTF-8') )
						return

					elif para["u"][0] == USER and para["p"][0] == PASS:

						relais_process = subprocess.Popen('unlock3s', shell=False, stdin=subprocess.PIPE)
						message = ''.join([
							'<html><body>CLIENT VALUES:<br>',
							'client_address=%s (%s)<br>' % (self.client_address,
														self.address_string()),
							'command=%s<br>' % self.command,
							'path=%s<br>' % self.path,
							'request_version=%s<br>' % self.request_version,
							'',
							'SERVER VALUES:<br>',
							'server_version=%s<br>' % self.server_version,
							'sys_version=%s<br>' % self.sys_version,
							'protocol_version=%s<br>' % self.protocol_version,
							'<br></body></html>',
							])
					else:
						message = ''.join([
							'<html><body><br>YOU ARE NOT COOKING!!',
							'</body></html>',
							])
				#send file content to client
				self.wfile.write( bytes(message, 'UTF-8') )
				rannum = random.getrandbits(64)
				print( rannum )
				qr.do( "https://%s:%d?c=%d" % ( HOST, PORT, rannum ), sys.path[0], self.op )
			
			return
            
		except IOError:
			self.send_error(404, 'file not found')



def serve(): 
			
	print( rannum )
	op = {'box_size': 4, 'pic': 'pic.png', 'template': 'template.png'}
	qr.do( "https://%s:%d?c=%d" % ( HOST, PORT, rannum ), sys.path[0], op )

	server_address = (HOST, PORT)
	httpd = http.server.HTTPServer(server_address, BinaryKitchenHTTPRequestHandler)
	httpd.socket = ssl.wrap_socket(httpd.socket,server_side=True,certfile='localhost.pem',ssl_version=ssl.PROTOCOL_TLSv1)
	print("serving on port", PORT)
	httpd.serve_forever()

serve()

