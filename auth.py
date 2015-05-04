#!/usr/bin/python

import sys,os
import ldap

SERVER = 'ldap.binary.kitchen'
PORT = 636

def auth( username, password ):

	dn = 'cn=%s,ou=Users,dc=binary-kitchen,dc=de' % username

	# ignore self-signed cert
	ldap.set_option( ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER )

	#con = ldap.initialize( SERVER, PORT )
	con = ldap.initialize( 'ldaps://%s:%d' % ( SERVER, PORT ) )

	try:

		con.bind_s( dn, password )

		return True
	
	except Exception:

		return False

	finally:

		con.unbind_s()

	return False


if __name__ == '__main__':

	username = sys.argv[ 1 ]
	password = sys.argv[ 2 ]

	if( auth( username, password ) ):
		os._exit( 0 )
	else:
		os._exit( 1 )


