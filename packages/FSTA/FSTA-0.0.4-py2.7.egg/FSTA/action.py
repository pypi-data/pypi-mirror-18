#!/usr/bin/env python
# -*- coding:utf-8 -*
from FSTA.installation import *
from FSTA.group import *
from FSTA.scenario import *
from FUTIL.my_logging import *
import socket

class action(object):
	"""action to be execute
	"""
	def __init__(self, callback = None, text = None):
		"""Initialisation
			- callback		function to be called
		"""
		self.callback = callback
		self._text = text
		
	@property
	def text(self):
		if self._text:
			return self._text
		else:
			return "* "
	
	def run(self, text):
		"""Run the callback fonction
		- text		phrase dicted
		"""
		try:
			self.callback()
		except BaseException as e:
			logging.error("Error on %s callback: %s"%(self.text, e))
		
		
class action_mqtt(action):
	""" mqtt order
	"""
	def __init__(self, topic, payload, qos = 0, retain = False, text = None):
		"""Initialisation
			- topic			mqtt topic
			- payload		mqtt payload
			- qos			mqtt qos
			- retain		mqtt retain
		"""
		self.topic = topic
		self.payload = payload
		self.qos = qos
		self.retain = retain
		self.installation = None
		self._text = text
	
	
	def run(self, text):
		""" Run the action
			- text		phrase dicted
		"""
		logging.info("Running action : " + self.text)
		try:
			self.installation.mqtt_client.reconnect()
			self.installation.mqtt_client.publish(self.topic, self.payload, self.qos, self.retain)
			self.installation.led.show_message(" ")
			self.installation.led.show_message(self.text)
		except socket.error:
			logging.error("Mqtt server : Connection refused")
			self.installation.led.show_message("X")