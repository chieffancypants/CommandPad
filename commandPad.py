#!/usr/bin/env python
# -*- coding: utf-8 -*-

import evdev
import sys
import os
from subprocess import Popen, PIPE, STDOUT

class CommandPad():

	buttonMode = 'A'									# Default to Mode A on the command pad
	uid = 1000											# The uid of the user to run the triggers as
	gid = 1000											# The gid of the group to run the triggers as
	commandPadName = 'Chicony USB Gaming Keyboard Pro'	# The name of the device (from ioctl)
	deviceGroup = None									# Placeholder for devices

	def getCommandPad(self):
		evDevs = []
		allEvDevs = os.listdir('/dev/input/')
		for evDev in allEvDevs:
			if 'event' in evDev:
				tmp = evdev.Device('/dev/input/' + evDev)
				if tmp.name == self.commandPadName:
					evDevs.append('/dev/input/' + evDev)

		return evDevs

	def capture(self):
		evDevs = self.getCommandPad()
		self.deviceGroup = evdev.DeviceGroup(evDevs)

		while 1:
			event = self.deviceGroup.next_event()
			if event is not None:
				if event.type == "EV_KEY" and event.value == 1:
					if event.code == 'BTN_TR2':
						self.buttonMode = 'A'
						print 'Mode ' + self.buttonMode
					elif event.code == 'BTN_SELECT':
						self.buttonMode = 'B'
						print 'Mode ' + self.buttonMode
					elif event.code.startswith("BTN"):
						self.trigger(event.code)

	def trigger(self, code):
		trigger_file = "%s/triggers/%s/%s.py" % (os.path.dirname(os.path.abspath(__file__)), self.buttonMode, self.buttonMap(code))

		if os.path.isfile(trigger_file):
			p = Popen(['python', trigger_file], stdout=PIPE, stdin=PIPE, stderr=STDOUT, preexec_fn=self.setPerms)
			#p = Popen(['env'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, preexec_fn=self.setPerms)
			#out = p.communicate()[0]
			#print(out)
		else: 
			print "No trigger file for Mode " + self.buttonMode + " -", self.buttonMap(code)

	def setPerms(self):
		os.setgid(self.gid)
		os.setuid(self.uid)

	def buttonMap(self, code):
		mapping = {
			'BTN_A': 1,
			'BTN_B': 2,
			'BTN_C': 3,
			'BTN_X': 4,
			'BTN_Y': 5,
			'BTN_Z': 6,
			'BTN_TL': 7,
			'BTN_TR': 8,
			'BTN_TL2': 9
		}
		return mapping[code]

if __name__ == "__main__":
	commandPad = CommandPad()
	try:
		commandPad.capture()
	except KeyboardInterrupt:
		commandPad.deviceGroup.close()
