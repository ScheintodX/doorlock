import time
import RPi.GPIO as GPIO


DOOR = 4
LOCK = 8

hightime = .2
lowtime = .4


def setup( pin ):
	GPIO.setmode( GPIO.BCM )
	GPIO.setup( pin, GPIO.OUT )


def high( pin ):
	GPIO.output( pin, GPIO.HIGH )


def low( pin ):
	GPIO.output( pin, GPIO.LOW )


def shutdown( pin ):
	GPIO.output( pin, GPIO.LOW )
	GPIO.setup( pin, GPIO.IN )


def open():

	setup( DOOR )

	# time to get to the door
	time.sleep( 1 )

	for i in range( 0, 3 ):

		high( DOOR )
		time.sleep( hightime )
		low( DOOR )
		time.sleep( lowtime )


def unlock():

	setup( LOCK )
	low( LOCK )


def lock():

	setup( LOCK )
	high( LOCK )

