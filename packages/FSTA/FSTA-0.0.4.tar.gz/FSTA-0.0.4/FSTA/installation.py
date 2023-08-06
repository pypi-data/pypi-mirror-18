#!/usr/bin/env python
# -*- coding:utf-8 -*


import sys
import signal
import time
import paho.mqtt.client as paho
import threading
import logging
import max7219.led as led
import speech_recognition as sr
import snowboydecoder

#TODO : plusieurs API (google, MS, ...) pour gérer quotas

class installation(object):
	"""A complete installation containing :
		- groups of scenarios with unique start hotword
		- mqtt serveur
	"""
	def __init__(self, groups = [], mqtt_host='localhost', mqtt_port = 1883, google_API_key = None, language = 'fr-FR', led = None, mqtt_base_topic = None, listen_timeout = 5):
		"""Initialisation
			- groups			list of groups of scenarios
			- mqtt_host			mqtt host (default localhost)
			- mqtt_port			mqtt port (default 1883)
			- google_API_key	google API key (32 car)
			- language			language for reconition (default : fr-Fr)
			- led				a max7219.led
		"""
		if isinstance(groups, list):
			self.groups = groups
		else:
			self.groups = [groups]
		self.hotwords = []
		self.callbacks = []
		self.mqtt_base_topic = mqtt_base_topic
		if self.mqtt_base_topic:
			if self.mqtt_base_topic[-1]!='/':
				self.mqtt_base_topic = self.mqtt_base_topic + '/'
		for group in self.groups:
			self.hotwords.append(group.hotword)
			self.callbacks.append(group.callback)
			group.init(self)
		self.mqtt_client = paho.Client()
		try:
			self.mqtt_client.connect(mqtt_host, mqtt_port, 30)
		except socket.error:
			logging.error("Mqtt server : Connection refused")
		self.interrupted = False
		self.on_action = False
		self.led = led
		self.led.brightness(0)
		self.google_API_key = google_API_key
		self.listen_timeout = listen_timeout
		self.language = language
		self.reconizer = sr.Recognizer()
		#self.calibrate()
		
				
		
	def run(self):
		"""Main function : wait for hotwords and run the callback function for the groups
		"""
		signal.signal(signal.SIGINT, self.signal_handler)
		while not self.interrupted:
			#TODO : analyse plugins
			self.detector = snowboydecoder.HotwordDetector(self.hotwords, sensitivity=0.5*len(self.hotwords))
			logging.debug("Detector start")
			self.on_action = False
			self.detector.start(detected_callback=self.callbacks,interrupt_check=self.interrupt_callback,sleep_time=0.03)
			logging.debug("Detector stopped")
		self.detector.terminate()
	
	def signal_handler(self, signal, frame):
		logging.info("installation interrupted by signal.")
		self.interrupted = True
	
	def interrupt_callback(self):
		return self.interrupted or self.on_action
		
	def calibrate(self):
		''' Calibrate the speech_recognition
		'''
		#TODO : faire aussi une calibration manuelle (qui sera appelée par la voix + enregistrement des paramètres sur fichier
		#Une autre solution est recognizer_instance.dynamic_energy_threshold = True (à voir...)
		with sr.Microphone() as source:
			logging.info("Calibration started ...")
			energy = self.reconizer.energy_threshold
			self.reconizer.adjust_for_ambient_noise(source)
			logging.info("energy_threshold is changed from %s to %s"%(energy, self.reconizer.energy_threshold))
	
	