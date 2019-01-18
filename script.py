#!/usr/bin/env python

'''
 ' Moisture sensing and watering routine for Farmbot
'''

import os, sys, json
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

input_errors = []
def qualify_int(package, name):
	data = get_config_value(package, name, int)
	try:
		data = int(data)
	except:
		input_errors.append('Must be integer for input: {}.'.format(name))
	else:
		return data

def qualify_sequence(seq_name):
	if len(''.join(seq_name.split())) > 0 and seq_name.lower() != 'none':
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None

def del_all_points(points):
	for point in points:
		try:
			app.delete('points', point['id'])
		except:
			device.log("App Error - Point ID: {}".format(point['id']), 'error')

PIN_LIGHTS = 7
PIN_WATER = 8
PKG = 'Water Routine'
Z_TRANSLATE = qualify_int(PKG, 'z_translate')
THRESHOLD = qualify_int(PKG, 'threshold')
NUM_READ = qualify_int(PKG, 'num_read')

weeder_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_moisture_retrieve', str))
weeder_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_moisture_return', str))
water_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_retrieve', str))
water_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_return', str))

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()

readings = []

device.write_pin(PIN_LIGHTS, 1, 0)
points = app.get_points()

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
