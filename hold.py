#!/usr/bin/env python3

import door
import time


door.setup( door.DOOR )
door.high( door.DOOR )

time.sleep( 5 )

door.low( door.DOOR )
