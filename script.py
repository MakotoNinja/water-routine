#!/usr/bin/env python

'''
 ' Moisture sensing and watering routine for Farmbot
'''

import os, sys, json
from random import randint
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

def take_readings():
	readings = []
	plants_chosen = []
	if device.get_current_position('x') > 10 or device.get_current_position('y') > 10 or device.get_current_position('z') > 0:
		device.home('all')
	device.execute(moisture_tool_retrieve_sequence_id)
	coord = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
	device.move_absolute(coord.get(), 100, coord.get_offset())
	for i in range(NUM_READ):
		rand_plant_num = randint(0, len(plants) - 1)
		while rand_plant_num in plants_chosen:
			rand_plant_num = randint(0, len(plants) - 1)
		plants_chosen.append(rand_plant_num)
		rand_plant = plants[rand_plant_num]
		device.log(json.dumps(rand_plant))
		# TODO random plant chosen, now offset coordinates and take moisture measurement

PIN_LIGHTS = 7
PIN_WATER = 8
PKG = 'Water Routine'
Z_TRANSLATE = qualify_int(PKG, 'z_translate')
THRESHOLD = qualify_int(PKG, 'threshold')
NUM_READ = qualify_int(PKG, 'num_read')

moisture_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_moisture_retrieve', str))
moisture_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_moisture_return', str))
water_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_retrieve', str))
water_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_return', str))
# TODO qualify each comma separated sequence
water_sequences = qualify_sequence(get_config_value(PKG, 'water_sequences', str))

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()

device.write_pin(PIN_LIGHTS, 1, 0)
plants = app.get_plants()

take_readings()

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
