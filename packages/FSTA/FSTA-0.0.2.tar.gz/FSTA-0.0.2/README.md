FSTA Lib  Fred Speech To Actions lib
========================================================================

	Based on snowboy hotword detection (https://snowboy.kitt.ai/)
	And cloud API like google speech API, Bing speech API, or ...

	Hardware :
		- Raspberry Pi (or other linux based device)
		- un good microphone (ie PS3 eye)
		- optional a matrix led max7219
		- a lot of iot (tv, ampli, RF-switch, lamp, garage door, ESP8266, arduino...
	
	Software :
		- lib FUTIL
		- snowboy decoder update here : http://docs.kitt.ai/snowboy/#downloads
		- python
		- optional mqtt server (like mosquitto)
		- optional node-RED
		

Installation :
     pip install FSTA
	 (create a /opt/FSTA directory for main program)
	 
Configuration :
	change config.py

 automatisation (jessie) :
	sudo systemctl enable maison.service
