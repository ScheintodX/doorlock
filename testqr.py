#!/usr/bin/env python3

import qr
import sys

OP = {'box_size': 4, 'pic': 'pic.png', 'template': 'template.png'}

qr.do( "blah" , sys.path[0], OP )
