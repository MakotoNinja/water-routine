#!/usr/bin/env python

from farmware_tools import device, app

class Coordinate:
	def __init__(self, x=0, y=0, z=0, ox=0, oy=0, oz=0):
		self.coordinate_node = device.assemble_coordinate(x, y, z)
		self.offset_node = device.assemble_coordinate(ox, oy, oz)

	def get_axis_position(self, axis):
		return self.coordinate_node['args'][axis]

	def set_axis_position(self, axis, pos):
		self.coordinate_node['args'][axis] = pos

	def get_coordinate(self):
		return self.coordinate_node['args']

	def set_coordinate(self, x=None, y=None, z=None):
		if x:
			self.coordinate_node['args']['x'] = x
		if y:
			self.coordinate_node['args']['y'] = y
		if z:
			self.coordinate_node['args']['z'] = z

	def get_node(self):
		return self.coordinate_node

	def get_offset_axis_position(self, axis):
		return self.offset_node['args'][axis]

	def set_offset_axis_position(self, axis, pos):
		self.offset_node['args'][axis] = pos

	def get_offset(self):
		return self.offset_node['args']

	def set_offset(self, x=None, y=None, z=None):
		if x:
			self.offset_node['args']['x'] = x
		if y:
			self.offset_node['args']['y'] = y
		if z:
			self.offset_node['args']['z'] = z

	def get_offset_node(self):
		return self.offset_node

	def move_abs(self, speed=100):
		device.move_absolute(self.coordinate_node, speed, self.offset_node)

	def print_me(self):
		print(self.get_coordinate())

	def print_offset(self):
		print(self.get_offset())
