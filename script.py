#!/usr/bin/env python

'''
 ' Moisture sensing and watering routine for Farmbot
'''

import os, sys, json
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate


def qualify_int(name):
	data = get_config_value(PKG, name, int)
	try:
		data = int(data)
	except:
		input_errors.append('Must be integer for input: {}.'.format(name))
	else:
		return data

def qualify_sequence(input_name):
	seq_name = get_config_value(PKG, input_name, str)
	if ''.join(seq_name.split()).lower() == 'none':
		input_errors.append('Encountered "None" for required sequence {}" '.format(input_name))
		return False
	elif len(''.join(seq_name.split())) > 0:
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None

def take_readings():
	plants_chosen = []
	device.execute(moisture_tool_retrieve_sequence_id)
	coord = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
	coord.move_abs()
	for i in range(NUM_SITES):
		rand_plant_num = randint(0, len(plants) - 1)
		while rand_plant_num in plants_chosen:
			rand_plant_num = randint(0, len(plants) - 1)
		plants_chosen.append(rand_plant_num)
		rand_plant = plants[rand_plant_num]
		device.log(json.dumps(rand_plant))
		coord.set_coordinate(rand_plant['x'], rand_plant['y'], Z_TRANSLATE)
		coord.set_offset(OFFSET_X, OFFSET_Y)
		coord.move_abs()
		coord.set_axis_position('z', SENSOR_Z_DEPTH)
		coord.move_abs()
		# take reading(s)
		for i in range(NUM_SAMPLES):
			reading = device.get_pin_value(PIN_SENSOR)
			device.log('Getting: {}'.format(reading))
			device.read_pin(PIN_SENSOR, 'Sensor', 1)
			moisture_readings.append(reading)
			device.wait(500)

		coord.set_axis_position('z', Z_TRANSLATE)
		coord.move_abs()
	#device.log('Readings Comkplete!', 'success')
	device.log('Readings: {}'.format(json.dumps(moisture_readings)), 'success')
	device.execute(moisture_tool_return_sequence_id)

def response():
	average = 0
	for i in moisture_readings:
		average += i
	average /= len(moisture_readings)
	if average < THRESHOLD:
		device.execute(water_tool_retrieve_sequence_id)
		device.execute(water_sequence_id)
		device.execute(water_tool_return_sequence_id)

PIN_LIGHTS = 7
PIN_SENSOR = 59
PIN_WATER = 8
PKG = 'Water Routine'

input_errors = []

SENSOR_Z_DEPTH = qualify_int('sensor_z_depth')
Z_TRANSLATE = qualify_int('z_translate')
OFFSET_X = qualify_int('offset_x')
OFFSET_Y = qualify_int('offset_y')
THRESHOLD = qualify_int('threshold')
NUM_SITES = qualify_int('num_sites')
NUM_SAMPLES = qualify_int('num_samples')

moisture_tool_retrieve_sequence_id = qualify_sequence('tool_moisture_retrieve')
moisture_tool_return_sequence_id = qualify_sequence('tool_moisture_return')
water_tool_retrieve_sequence_id = qualify_sequence('tool_water_retrieve')
water_tool_return_sequence_id = qualify_sequence('tool_water_return')
water_sequence_id = qualify_sequence('water_sequence')

moisture_readings = []

if len(input_errors):
	for err in input_errors:
		device.log(err, 'warn')
	device.log('Fatal errors occured, farmware exiting.', 'warn')
	sys.exit()
if device.get_current_position('x') > 10 or device.get_current_position('y') > 10 or device.get_current_position('z') < -10:
	device.home('all')

device.log('Read Pin: {}'.format(device.read_pin(PIN_SENSOR, 'Sensor', 1)))

device.write_pin(PIN_LIGHTS, 1, 0)
plants = app.get_plants()

take_readings()
response();

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
