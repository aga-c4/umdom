#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# pip3 install telebot, requests

# Рутовая папка - корень проекта, мы находимся в папке бота умного дома
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import telebot

from config import custom, defaultbot
from models.config import Config
from bots.umdom.models.botdevice import BotDevice
from models.mybot import MyBot

config = Config(custom=custom, 
                defaultbot=defaultbot, 
                allow_configs=["main", "botstru", "devices"]) 
my_bot = MyBot(config)

bot = telebot.TeleBot(config.get_config()["telegram"]["api_token"])
mess_txt = config.get_config()["bot"]["name"]+":\n"
mess_txt += "---------------\n"
for device_alias in my_bot.devices:
    dev_model = BotDevice(my_bot, my_bot.devices, device_alias)
    mess_txt += dev_model.get_info_message()
    mess_txt += "---------------\n"

bot.send_message(config.get_config()["telegram"]["channels"]["domchat"], text=mess_txt)
