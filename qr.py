#!/usr/bin/env python
"""
qr - Convert stdin (or the first argument) to a QR Code.

When stdout is a tty the QR Code is printed to the terminal and when stdout is
a pipe to a file an image is written. The default image format is PNG.
"""
import sys, os
import optparse
import qrcode
from PIL import Image
import subprocess

def do( url, pathname, opts ): 
	x, y = 264, 176

	if opts['box_size']:
		print( int(opts['box_size']) )
		qr = qrcode.QRCode( error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=int(opts['box_size']),border=2,)
	else:
		qr = qrcode.QRCode( error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=4,border=2,)

	if url is not None:
		qr.add_data( url )
	else:
		qr.add_data(sys.stdin.read())

	#pathname = os.path.dirname(sys.argv[0])
	print( "Start CMD for SPI and I2C " + str( subprocess.Popen("gpio load spi; gpio load i2c", shell=True, executable="/bin/bash") ) )

	if sys.stdout.isatty():
		qr.print_tty()
		newImg = Image.new('1', (x,y))
		im = Image.open(opts['template'])
		newImg.paste(im, (0,0))
		img = qr.make_image(image_factory=None)
		width, height = img.size
		offset_y = (y-height)/2
		newImg.paste( img, (int(x-(width)),int(y-(height)-offset_y)) )
		newImg.save( opts['pic'] )
		newImg.save( "test.xbm" )
		pixels = list(newImg.getdata())
		pic_hex = newImg.tostring( 'xbm' ).decode().replace( ",", " " ).replace( "0x", "" ).replace( "\n", "" )
		epaper_process = subprocess.Popen(pathname+'/epaper', shell=False, stdin=subprocess.PIPE)
		epaper_process.communicate( bytearray.fromhex( pic_hex ) )
		return

	else:
		newImg = Image.new('1', (x,y))
		im = Image.open(opts['template'])
		newImg.paste(im, (0,0))
		img = qr.make_image(image_factory=None)
		width, height = img.size
		offset_y = (y-height)/2
		newImg.paste( img, (int(x-(width)),int(y-(height)-offset_y)) )
		newImg.save( opts['pic'] )
		newImg.save( "test.xbm" )
		pixels = list(newImg.getdata())
		pic_hex = newImg.tostring( 'xbm' ).decode().replace( ",", " " ).replace( "0x", "" ).replace( "\n", "" )
		epaper_process = subprocess.Popen(pathname+'/epaper', shell=False, stdin=subprocess.PIPE)
		epaper_process.communicate( bytearray.fromhex( pic_hex ) )
		return

def main(*args):
	parser = optparse.OptionParser(usage=__doc__.strip())
	parser.add_option("-b", "--box_size", type="int",dest="box_size", help="The size of one QRcode dot [4]", default=4)
	parser.add_option("-p", "--pic", type="string",dest="pic", help="the picture to save [pic.png]", default="pic.png" )
	parser.add_option("-t", "--template", type="string",dest="template", help="the Templatepicture [template.png]", default="template.png" )
	opts, args = parser.parse_args(list(args))
	print( opts )
	do( args[0], sys.path[0], opts )


if __name__ == "__main__":
	main(*sys.argv[1:])
