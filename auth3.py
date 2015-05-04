#!/usr/bin/python3

import subprocess

SERVER = 'ldap.binary.kitchen'
PORT = 636

# Python3 ldap3 sux. Aufrufen des python2 skripts per console

def auth( username, password ):

	print( username, password )

	res = subprocess.call( [ "/home/pi/lock/auth.py", username, password ] )

	print( res )

	return res == 0


if __name__ == '__main__':

	print( auth( 'flo', 'blah' ) ) #--> false
	print( auth( 'flo', 'xxxxxxxx' ) )
