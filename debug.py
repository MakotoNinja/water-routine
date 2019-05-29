#!/usr/bin/env python

from farmware_tools import device, app

debug_flag = False

def log(msg):
	if debug_flag:
		device.log(msg)
