#!/usr/bin/env python

from farmware_tools import device, app

class Coordinate:
	def __init__(self, x=0, y=0, z=0, ox=0, oy=0, oz=0):
		self.coordinate = device.assemble_coordinate(x, y, z)
		self.offset = device.assemble_coordinate(ox, oy, oz)

	def set_pos(self, axis, pos):
		self.coordinate['args'][axis] = pos

	def get_pos(self, axis):
		return self.coordinate['args'][axis]

	def set_coordinate(self, x=None, y=None, z=None):
		if x:
			self.coordinate['args']['x'] = x
		if y:
			self.coordinate['args']['y'] = y
		if z:
			self.coordinate['args']['z'] = z

	def get_coordinate(self):
		return self.coordinate['args']

	def get_node(self):
		return self.coordinate

	def get_offset_pos(self, axis):
		return self.offset['args'][axis]

	def set_offset_pos(self, axis, pos):
		self.offset['args'][axis] = pos

	def get_offset(self):
		return self.offset['args']

	def get_offset_node(self):
		return self.offset

	def set_offset(self, x=None, y=None, z=None):
		if x:
			self.offset['args']['x'] = x
		if y:
			self.offset['args']['y'] = y
		if z:
			self.offset['args']['z'] = z

	def print_me(self):
		print(self.get_coordinate())

	def print_offset(self):
		print(self.get_offset())
