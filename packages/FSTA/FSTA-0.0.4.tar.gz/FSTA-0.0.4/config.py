#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.group import *
from FSTA.scenario import *

from FUTIL.my_logging import *
import json

#TODO : plutôt utiliser des plugins soit en lecture de json (ou autre), soit directement du code python (peut être plus simple)
#	maison.group
#		Un ou plusieurs groupes (nom, hotword)
#		ex : {'name' : "Maison", 'hotword' : "./resources/maison.pmdl"}
#	lumiere_on.scene
#		Un ou plusieurs scenarios
#		ex : {'name' : "LUMIERE ON", 'phrases' : {"Allume la lumière","lumière s'il te plaît","lumière"}, ....
#
#ou en code direct
#		maison = group(....)
#		lumiere_on = scenario(...)
#
#	Le programme scrute régulièrement le repertoire des plugin et les applique (mais il va falloir metre des try !)

def get_installation():
	return installation(
		groups = [
			group(name = "Maison",
				hotword = "./resources/Hotworks/maison.pmdl",
				scenarios = [
							scenario(name = "LUMIERE ON",
									phrases = [u"Allume la lumière",
												u"lumière s'il te plaît",
												u"lumière"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/LUMIERES",
											payload = "ON",
											text = "ON")),
							scenario(name = "LUMIERE OFF",
									phrases = [u"éteins la lumière",
												u"coupe la lumière"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/LUMIERES",
											payload = "OFF",
											text = "OFF")),
							scenario(name = "MUSIQUE ON",
									phrases = [u"musique",
												u"allume la musique"],
									actions = action_mqtt(
											topic = "T-HOME/SQUEEZE/PISQUEEZE",
											payload = "play",
											text = "Musique")),
							scenario(name = "MUSIQUE OFF",
									phrases = [u"stop la musique",
												u"éteins la musique",
												u"arrête la musique"],
									actions = action_mqtt(
											topic = "T-HOME/SQUEEZE/PISQUEEZE",
											payload = "stop",
											text = "STOP")),
							scenario(name = "MUSIQUE NEXT",
									phrases = [u"musique suivante",
												u"change la musique"],
									actions = action_mqtt(
											topic = "T-HOME/SQUEEZE/PISQUEEZE",
											payload = "button,jump_fwd",
											text = "Next")),
							scenario(name="VOLUME +",
									phrases = [u"augmente le volume",
												u"plus fort"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/DENON",
											payload = "MVUP",
											text = "+")),
							scenario(name = "VOLUME -",
									phrases = [u"baisse le volume",
												u"moins fort"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/DENON",
											payload = "MVDOWN",
											text = "-")),
							scenario(name = "TV OFF",
									phrases = [u"éteins la télé",
												u"coupe la télé"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/TV",
											payload = "KEY_POWEROFF",
											text = "+")),
							scenario(name="REBOOT KODI",
									phrases = u"reboot Kodi",
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = "REBOOT",
											text = "Reboot Kodi")),
							scenario(name = "Heure",
									phrases = [u'quelle heure est-il', u'il est quelle heure'],
									actions = action_mqtt(
											topic = 'T-HOME/QUESTION',
											payload = "HEURE")),
							scenario(name = "date",
									phrases = [u'quel jour sommes nous', u'quelle est la date', u'Quand sommes nous'],
									actions = action_mqtt(
											topic = 'T-HOME/QUESTION',
											payload = "DATE")),
							scenario(name = "Fuel",
									phrases = [u'Combien de fioul', u'Quantité de fioul', u'Cuve fioul', u'fioul'],
									actions = action_mqtt(
											topic = 'T-HOME/QUESTION',
											payload = "FUEL"))
								]),
			group(name = "KODI",
				hotword = "./resources/Hotworks/Ok Kodi.pmdl",
				scenarios = [
							scenario(name = "REBOOT",
									phrases = u"reboot",
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = "REBOOT",
											text = "Reboot Kodi")),
							scenario(name="PLAY-PAUSE",
									phrases = [u"pause",u"pose",
												u"enlève pause", u"enlève pose"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = json.dumps({
													"cmd": "Player.PlayPause",
													"args" :{
														"playerid": 1
														}
													}),
											text = "Pause")),
							scenario(name="STOP",
									phrases = [u"stoppe",u"stop",
												u"arrête film"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = json.dumps({
													"cmd": "Player.Stop",#Attention si Kodi en pause, le Stop ne fonctionne pas! TODO ....
													"args" :{
														"playerid": 1
														}
													}),
											text = "Stop")),
							scenario(name="ETEINT TOUT",
									phrases = [u"éteins tous", u"éteins toi "],
									actions = [action_mqtt(
													topic = "T-HOME/SALON/TV",
													payload = "KEY_POWEROFF",
													text = "Stop TV"),
												action_mqtt(
													topic = "T-HOME/SALON/KODI",
													payload = json.dumps({
															"cmd": "Player.Stop",
															"args" :{
																"playerid": 1
																}
															}),
													text = "Stop Kodi")
												]
										)
								])],
		mqtt_host='192.168.10.155',
		led = led.matrix(),
		google_API_key = "AIzaSyDtizHAgEhUw5WjW9aRs84GUNk7o-fXwvA",
		mqtt_base_topic = 'T-HOME/SALON/LISTEN')