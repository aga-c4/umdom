#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# pip3 install redis, paho-mqtt

# Рутовая папка - корень проекта, мы находимся в папке бота умного дома
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import logging
import paho.mqtt.client as mqtt
import json

from agaunibot.botapp import BotApp
from agaunibot.config import Config
from agaunibot.mybot import MyBot
from agaunibot.botcache import BotCache
from app.models.botdevice import BotDevice

logging.basicConfig(level=logging.INFO)

params = BotApp.get_console_commands()      
custom = params.get("custom", "")    
defconfig = params.get("defconfig", "default")
print(f"Try to run bot with custom {custom}") 

conf_obj = Config(custom=custom, 
                  defconfig=defconfig, 
                  allow_configs=["main", "botstru", "devices"]) 

config = conf_obj.get_config("main")
my_bot = MyBot(conf_obj)
devicecache_conf = config.get("system",{}).get("devicecache", {})
bcache = BotCache(host=devicecache_conf.get("host", "127.0.0.1"), 
                  port=devicecache_conf.get("port", 6379), 
                  db=devicecache_conf.get("db", 0))

# Опрос устройств, по которым можно обновить статусы (разного рода выключатели)
for device_alias, device in my_bot.devices.items():
    dev_model = BotDevice(my_bot, my_bot.devices, device_alias)
    if not dev_model.model is None \
        and device.get("model")=="ZigbeeDevice" \
        and type(device.get("commands", False)) is dict:
        dev_model.set({ "state": "" })


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("zigbee2mqtt/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic.find("zigbee2mqtt/bridge")==-1:
        # print("---[", msg.topic, "]---")
        # print(type(msg.payload.decode("utf-8")))
        payload = msg.payload.decode("utf-8")
        if payload is None:
            value = payload
        else:
            try:
                value = json.loads(payload)        
            except:
                value = payload    
        if not value is None and not msg.topic is None and not msg.topic=="":
            bcache.set(msg.topic, value)
            # print(msg.topic, bcache.get(msg.topic))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqtt_conf = config.get("system",{}).get("mqtt", {})
host=mqtt_conf.get("host", "127.0.0.1")
port=mqtt_conf.get("port", 1883)
username=mqtt_conf.get("username", "")         
password=mqtt_conf.get("password", "")         
qos=mqtt_conf.get("qos", 1)         

if username!="" and password!="":
    mqttc.username_pw_set(username=username, password=password)

try:
    mqttc.connect(host, port, 60)
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttc.loop_forever()
except:
    pass