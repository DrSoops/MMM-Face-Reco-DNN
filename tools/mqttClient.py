import paho.mqtt.client as paho
import json
import sys

def convertMessage(type, message):
        return json.dumps({"action":type, "section":"mqtt", "message":message})

def printjson(type, message):
	print(convertMessage(type, message))
	sys.stdout.flush()

def on_connect(client, userdata, flags, rc):
	message = {
		"type": "connection",
		"rc": rc
	}
	if rc == 0:
		message["status"] = "connected"
	else:
		message["status"] = "error"
	printjson("status", message)

def on_disconnect(client, userdata, rc):
	message = {
		"type": "disconnection",
		"rc": rc
	}
	if rc == 0:
		message["status"] = "graceful"
	else:
		message["status"] = "error"
	printjson("status", message)

class Client(paho.Client):
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.on_connect=on_connect
		self.on_disconnect=on_disconnect

	def start(self, host, port):
		self.connect(host, port)
		self.loop_start()

	def stop(self):
		self.loop_stop()
		self.disconnect()
