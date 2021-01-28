import argparse
import json
import mqttClient as mqc
import time

def on_login(users):
        convertedUsers = []
        for user in users:
                loggedInUser = loggedInUsers.get(user)
                if loggedInUser is None:
                        loggedInUser = {"count":0,"ids":[]}
                        convertedUsers.append(user)
                loggedInUser["count"] = loggedInUser["count"] + 1;
                loggedInUsers[user] = loggedInUser
                print("User:", user, "count:", loggedInUser["count"])
        if convertedUsers:
                print("New login users:", convertedUsers)
                message = {"action":"login", "message":{"users":convertedUsers}}
                mqttClient.publish(args["mqttTopic"], json.dumps(message))

def on_logout(users):
        convertedUsers = []
        for user in users:
                loggedInUser = loggedInUsers.get(user)
                if loggedInUser is not None:
                        loggedInUser["count"] = loggedInUser["count"] - 1;
                        print("User:", user, "count:", loggedInUser["count"])
                        if loggedInUser["count"] <= 0:
                                del loggedInUsers[user]
                                convertedUsers.append(user)
                        else:
                                loggedInUsers[user] = loggedInUser
        if convertedUsers:
                print("New logout users:", convertedUsers)
                message = {"action":"logout", "message":{"users":convertedUsers}}
                mqttClient.publish(args["mqttTopic"], json.dumps(message))

def on_message_msgs(mosq, obj, msg):
        # TODO: Parse out json
        # Add camera identifier to json?
        # Add to Login list if login
        # Remove count from login list if logout
        jsonMessage = json.loads(msg.payload)
        action = jsonMessage["action"]
        print("Action: " + action)
        if(action == "login"):
                on_login(jsonMessage["message"]["users"])
        elif(action == "logout"):
                on_logout(jsonMessage["message"]["users"])

print("Started")
loggedInUsers = {}
ap = argparse.ArgumentParser()
ap.add_argument("-mqh", "--mqttHost", type=str, required=False, default="eclipse-mosquitto",
        help="MQTT server address or IP")
ap.add_argument("-mqp", "--mqttPort", type=int, required=False, default=1883,
        help="MQTT server Port")
ap.add_argument("-mqt", "--mqttTopic", type=str, required=False, default="facialrecognition/converted",
        help="MQTT topic to publish messages to")
ap.add_argument("-mqts", "--mqttTopicSub", type=str, required=False, default="facialrecognition/raw",
        help="MQTT topic to publish messages to")
# TODO: Add generic MQTT options param in json form to support ssl certs/self signed certs
args = vars(ap.parse_args())

mqttClient = mqc.Client("converter-facial-rec", clean_session=False)
mqttClient.message_callback_add(args["mqttTopicSub"], on_message_msgs)
mqttClient.subscribe(args["mqttTopicSub"])
print("Connecting to mqtt client {}:{}".format(args["mqttHost"], args["mqttPort"]))
mqttClient.start_forever(args["mqttHost"], args["mqttPort"])