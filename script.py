#!/usr/bin/env python

'''
 ' Moisture sensing and watering routine for Farmbot
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

def take_readings():
	plants_chosen = []
	device.execute(moisture_tool_retrieve_sequence_id)
	#coord = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
	#device.log('Creating Coordinate')
	bot = Coordinate(device.get_current_position('x'), device.get_current_position('y'))
	bot.set_offset(OFFSET_X, OFFSET_Y, move_abs=False) # sets the offset, auto-move disabled
	#device.log('BOT: {}'.format(bot))
	for i in range(NUM_SITES):
		rand_plant_num = randint(0, len(target_plants) - 1)
		while rand_plant_num in plants_chosen:
			rand_plant_num = randint(0, len(target_plants) - 1)
		plants_chosen.append(rand_plant_num)
		rand_plant = target_plants[rand_plant_num]
		device.log('Random Plant: {}'.format(json.dumps(rand_plant)))

		bot.set_axis_position('z', Z_TRANSLATE)					# sets the z axis to translate height, auto-move enabled
		bot.set_coordinate(rand_plant['x'], rand_plant['y'])	# set the plant coordinate, auto-move enabled
		bot.set_axis_position('z', SENSOR_Z_DEPTH)				# plunge sensor into soil, auto-move enabled
		# take reading(s)
		site_readings = []
		for j in range(NUM_SAMPLES):
			device.read_pin(PIN_SENSOR, 'Sensor', 1)
			site_readings.append(device.get_pin_value(PIN_SENSOR))
			device.wait(100)
		average = 0
		for reading in site_readings:
			average += reading
		average /= NUM_SAMPLES
		moisture_readings.append(average)
		device.log('Site Reading #{}: {}'.format(i, average), 'success')
	bot.set_axis_position('z', Z_TRANSLATE)
	device.log('Readings: {}'.format(json.dumps(moisture_readings)), 'success')
	device.execute(moisture_tool_return_sequence_id)

def response():
	average = 0
	for i in moisture_readings:
		average += i
	average /= len(moisture_readings)
	device.log('Total Moisture Average: {}'.format(average), 'info')
	if average < THRESHOLD:
		device.execute(water_tool_retrieve_sequence_id)
		device.execute(water_sequence_id)
		device.execute(water_tool_return_sequence_id)

PIN_LIGHTS = 7
PIN_SENSOR = 59
PIN_WATER = 8
PKG = 'Water Routine'

device.log('BEGIN FARMWARE: {}'.format(PKG))

input_errors = []
PLANT_TYPES = Qualify.get_csv(PKG, 'plant_types')
device.log('PLANT TYPES: {}'.format(PLANT_TYPES))
SENSOR_Z_DEPTH = Qualify.integer(PKG, 'sensor_z_depth')
Z_TRANSLATE = Qualify.integer(PKG,'z_translate')
OFFSET_X = Qualify.integer(PKG,'offset_x')
OFFSET_Y = Qualify.integer(PKG,'offset_y')
THRESHOLD = Qualify.integer(PKG,'threshold')
NUM_SITES = Qualify.integer(PKG,'num_sites')
NUM_SAMPLES = Qualify.integer(PKG,'num_samples')
#device.log('Integers Qualified')
moisture_tool_retrieve_sequence_id = Qualify.sequence(PKG, 'tool_moisture_retrieve')
moisture_tool_return_sequence_id = Qualify.sequence(PKG, 'tool_moisture_return')
water_tool_retrieve_sequence_id = Qualify.sequence(PKG, 'tool_water_retrieve')
water_tool_return_sequence_id = Qualify.sequence(PKG, 'tool_water_return')
water_sequence_id = Qualify.sequence(PKG, 'water_sequence')
#device.log('Sequences Qualified')
moisture_readings = []

if len(input_errors):
	for err in input_errors:
		device.log(err, 'warn')
	device.log('Fatal config errors occured, farmware exiting.', 'warn')
	sys.exit()
else:
	device.log('No config errors were detected.', 'success')

if device.get_current_position('x') > 10 or device.get_current_position('y') > 10 or device.get_current_position('z') < -10:
	device.home('all')

device.write_pin(PIN_LIGHTS, 1, 0)

target_plants = []
all_plants = app.get_plants()
device.log('(0) All Plants: {}'.format(json.dumps(all_plants)))
for plant in all_plants:
	device.log('plant[\'NAME\']: {}'.format(plant['NAME']))
	plant_name = ''.join(plant['NAME'].split()).lower()
	device.log('plant name: {}'.format(plant_name))
	if plant_name in PLANT_TYPES:
		target_plants.append(plant)
device.log('Target Plants: {}'.format(json.dumps(target_plants)))
take_readings()
response();

device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
device.log('END FARMWARE: {}'.format(PKG))
