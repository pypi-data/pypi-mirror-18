#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.scenario import *
from FUTIL.my_logging import *
import socket

class group(object):
	"""A group of scenarios with a unique hotword
	"""
	def __init__(self, 
					name, 
					hotword = "./resource/snowboy.umdl", 
					mqtt_hotword_topic = None, 
					scenarios = []):
		"""Initialisation
			- hotword			string containing path to a umdl or pmdl file as "Ok google" 
			- orders			list of order object
		"""
		self.name = name
		self.hotword = hotword
		if isinstance(scenarios, list):
			self.scenarios = scenarios
		else:
			self.scenarios = [scenarios]
		self.installation = None
		self.mqtt_hotword_topic = mqtt_hotword_topic
		
	def init(self, installation):
		'''Initialise the group with installation datas
		'''
		self.installation = installation
		for scenario in self.scenarios:
			scenario.init(self)		
		if self.mqtt_hotword_topic == None and installation.mqtt_base_topic :
			self.mqtt_hotword_topic = installation.mqtt_base_topic + self.name
	
	def callback(self):
		""" Function called when the hotword match
		"""
		logging.info(self.name + " : I listen ...")
		if self.mqtt_hotword_topic:
			try:
				self.installation.mqtt_client.reconnect()
				self.installation.mqtt_client.publish(self.mqtt_hotword_topic, self.name)
			except socket.error:
				logging.error("Mqtt server : Connection refused")
				logging.error("Mqtt server : Connection refused")
		self.installation.on_action = True
		self.installation.detector.terminate()
		self.installation.led.show_message("^")
		self.installation.calibrate()
		self.installation.led.show_message("O")
		time.sleep(0.1)
		text = None
		try:
			with sr.Microphone() as source:
				audio = self.installation.reconizer.listen(source, self.installation.listen_timeout)
			logging.info("Audio captured")
			self.installation.led.show_message("@")
			#Google API
			try:
				text =  self.installation.reconizer.recognize_google(audio, key=self.installation.google_API_key, language = self.installation.language)
				logging.info("Text found with Google API: " + text)
			except sr.UnknownValueError:
				logging.warning("Google Speech Recognition could not understand audio")
			except sr.RequestError as e:
				logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))
			#TODO : utiliser d'autres API
		except Exception as e:
			logging.warning("Audio capture error : %s"%(e.message))
		if text:
			for scenario in self.scenarios:
				scenario.test(text)
			#Tri des résultats
			results = sorted(self.scenarios, key = lambda scenario:-scenario.valide)
			if results[0].valide:
				results[0].run(text)
			else:
				self.installation.led.show_message("?")
				logging.info("The text no math with scenarios.")
				time.sleep(0.5)
		else:
			self.installation.led.show_message("#")
			logging.info("None text captured.")
			time.sleep(0.5)
		self.installation.led.show_message(" ")
		
