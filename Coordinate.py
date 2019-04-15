#!/usr/bin/env python

from farmware_tools import device, app

class Coordinate:
	def __init__(self, x=0, y=0, z=0, ox=0, oy=0, oz=0, speed=100):
		self.coordinate_node = device.assemble_coordinate(x, y, z)
		self.offset_node = device.assemble_coordinate(ox, oy, oz)
		self.speed = speed

	def get_axis_position(self, axis):
		return self.coordinate_node['args'][axis]
	'''
	 ' @axis - str - can only be 'x', 'y' or 'z'
	 ' @pos  - int - number in millimeters to position axis
	'''
	def set_axis_position(self, axis, pos, move_abs=True):
		self.coordinate_node['args'][axis] = pos
		if move_abs:
			self.move_abs()

	def get_coordinate(self):
		return self.coordinate_node['args']

	def set_coordinate(self, x=None, y=None, z=None, move_abs=True):
		if x:
			self.coordinate_node['args']['x'] = x
		if y:
			self.coordinate_node['args']['y'] = y
		if z:
			self.coordinate_node['args']['z'] = z
		if move_abs:
			self.move_abs()

	def get_node(self):
		return self.coordinate_node

	def get_offset_axis_position(self, axis):
		return self.offset_node['args'][axis]

	def set_offset_axis_position(self, axis, pos, move_abs=True):
		self.offset_node['args'][axis] = pos
		if move_abs:
			self.move_abs()

	def get_offset(self):
		return self.offset_node['args']

	def set_offset(self, x=None, y=None, z=None, move_abs=True):
		if x:
			self.offset_node['args']['x'] = x
		if y:
			self.offset_node['args']['y'] = y
		if z:
			self.offset_node['args']['z'] = z
		if move_abs:
			self.move_abs()

	def get_offset_node(self):
		return self.offset_node

	def move_abs(self, speed=None):
		if speed:
			self.set_speed(speed)
		device.move_absolute(self.coordinate_node, self.speed, self.offset_node)

	def set_speed(self, speed):
		self.speed = speed

	def get_speed(self):
		return self.speed

	def print_me(self):
		print('Coordinate: {}, Offset: {}'.format(self.get_coordinate(), self.get_offset()))

	def print_offset(self):
		print(self.get_offset())
