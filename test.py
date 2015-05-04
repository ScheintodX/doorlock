#!/usr/bin/env python3

import door
import time
import qr

PIN = 8

qr.init()

'''
while True:

	try:

		door.setup( PIN )

		print( "Lock" )
		door.high( PIN )
		time.sleep( .5 )

		print( "Unlock" )
		door.low( PIN )
		time.sleep( .5 )


	finally:

		door.shutdown( PIN )
'''
