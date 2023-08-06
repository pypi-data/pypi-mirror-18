#!/usr/bin/env python
# -*- coding:utf-8 -*


#TODO : ré-ecrire en object

import paho.mqtt.client as mqtt
from FUTIL.my_logging import *

MODE = 'gTTS' # for Google API
# MODE = pyttsx

if MODE == 'pyttsx':
	import pyttsx
if MODE == 'gTTS':
	from gtts import gTTS
	import os



my_logging(console_level = DEBUG, logfile_level = DEBUG, details = False)

mqtt_host = '192.168.10.155'
mqtt_port = 1883
if MODE == 'pyttsx':
	language = 'french'
	rate = 120
if MODE == 'gTTS':
	language = 'fr'
topic = 'T-HOME/PI-SALON/SPEAK'

if MODE == 'pyttsx':
	engine = pyttsx.init()
	engine.setProperty('rate', rate)
	engine.setProperty('voice', language)

def speak(text):
	if MODE == 'pyttsx':
		engine.say(text)
		engine.runAndWait()
		logging.info("'%s' speaked with pyttsx."%(text))
	if MODE == 'gTTS':
		try:
			gTTS(text=text, lang=language).save("tts.mp3")
			os.system('mpg123 tts.mp3')
			logging.info("'%s' speaked with gTTS."%(text))
		except Exception as e:
			logging.warning(e.message)
	
def on_mqtt_message(client, userdata, msg):
	logging.info("MQTT : %s => %s"%(msg.topic, msg.payload))
	speak(msg.payload)

def on_mqtt_connect(client, userdata, flags, rc):
	logging.info("MQTT connection.")
	mqttc.message_callback_add(topic, on_mqtt_message)
	mqttc.subscribe(topic)
	
def on_mqtt_disconnect(client, userdata, rc):
	if rc != 0:
		logging.warning("MQTT : Unexpected disconnection.")
		mqttc.reconnect()
	else:
		logging.info("MQTT disconnection.")



		
mqttc = mqtt.Client()
mqttc.connect(mqtt_host, mqtt_port)
mqttc.on_connect = on_mqtt_connect
mqttc.on_disconnect = on_mqtt_disconnect
mqttc.message_callback_add(topic, on_mqtt_message)
speak("Salut les amis. Je suis a votre service.")
mqttc.loop_forever()