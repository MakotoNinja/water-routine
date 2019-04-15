#!/usr/bin/env python

from farmware_tools import device, app, get_config_value

errors = []
def combo(PKG, input_name):
	string = get_config_value(PKG, input_name, str)
	string = ''.join(string.split(' ')).lower()
	if string == 'none':
		errors.append('Encountered "None" for required sequence {}" '.format(input_name))
		return None
	elif ',' not in string:
		errors.append('Combo field does not contain a comma: {}'.format(input_name))
		return None
	else:
		split = string.split(',')
		if split[0] not in 'xy':
			errors.append('Left side of comma must be "X" or "Y". Found: {}'.format(split[0]))
		try:
			split[1] = int(split[1])
		except:
			errors.append('Right side of comma should be an Integer. Found: {}'.format(split[1]))
		return {'axis' : split[0], 'value' : split[1]}

def integer(PKG, input_name):
	data = get_config_value(PKG, input_name, int)
	try:
		data = int(data)
	except:
		errors.append('Must be integer for input: {}.'.format(input_name))
	else:
		return data

def sequence(PKG, input_name):
	seq_name = get_config_value(PKG, input_name, str)
	if ''.join(seq_name.split()).lower() == 'none':
		errors.append('Encountered "None" for required sequence {}" '.format(input_name))
		return False
	elif len(''.join(seq_name.split())) > 0:
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None

def get_csv(PKG, input_name):
	string = get_config_value(PKG, input_name, str)
	return ''.join(string.split()).lower().split(',')

def get_tool(id):
	tools = app.get_toolslots()
	for tool in tools:
		if tool['tool_id'] == id:
			 return tool
	return None
