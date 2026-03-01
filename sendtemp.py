#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# pip3 install telebot, requests

# Рутовая папка - корень проекта, мы находимся в папке бота умного дома
# import os
# import sys
# path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
# if not path in sys.path:
#     sys.path.insert(1, path)
# del path

from agaunibot.botapp import BotApp
from agaunibot.config import Config
from app.models.botdevice import BotDevice
from agaunibot.mybot import MyBot

params = BotApp.get_console_commands()      
custom = params.get("custom", "")    
defconfig = params.get("defconfig", "default")
print(f"Try to run bot with custom {custom}") 

config = Config(custom=custom, 
                  defconfig=defconfig, 
                  allow_configs=["main", "botstru", "devices"]) 
my_bot = MyBot(config)

bot = telebot.TeleBot(config.get_config()["telegram"]["api_token"])
mess_txt = config.get_config()["bot"]["name"]+":\n"
mess_txt += "---------------\n"
for device_alias in my_bot.devices:
    dev_model = BotDevice(my_bot, my_bot.devices, device_alias)
    mess_txt += dev_model.get_info_message()
    mess_txt += "---------------\n"

mess_txt="test"
bot.send_message(config.get_config()["telegram"]["channels"]["domchat"], text=mess_txt)
