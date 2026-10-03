from agaunibot.request import Request
import logging
import json
import os
from datetime import datetime
from time import sleep

from agaunibot.botapp import app
from app.models.botdevice import BotDevice
from app.models.botlocation import BotLocation

class DevicesController:

    def __init__(self):
        self.message = app.message

    def get_info(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:get_info")
        location_alias = request.session.get("location", "")
        logging.info(str(request.user.id)+f": location_alias:{location_alias}")
        mess_txt = request.bot.config["bot"]["name"]+":\n"
        mess_txt = ""
        for device_alias in request.bot.devices:
            dev_model = BotDevice(request.bot, request.bot.devices, device_alias)
            if not dev_model.model is None and not request.user is None \
                and request.user.has_role(dev_model.access.get("view", None)) \
                and dev_model.in_location(location_alias):
                mess_txt += dev_model.get_info_message("mini")
                mess_txt += "-----------\n"
        self.message.send(request.chatid, text=mess_txt)

    def zigbee_pairing_mode(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:use_pairing_mode")
        dev_model = BotDevice(request.bot, {}, "")
        dev_model.use_pairing_mode()    
        mess_txt = "Включен режим поиска zigbee устройств на 254 секунды"
        self.message.send(request.chatid, text=mess_txt)

    def list(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:list")
        location_alias = request.session.get("location", "")
        logging.info(str(request.user.id)+f": location_alias:{location_alias}")
        command = request.message.command
        device_alias = request.message.command_obj
        command_alias = request.message.command_info

        if request.is_script_command and command=="command":
            dev_model = BotDevice(request.bot, request.bot.devices, device_alias)
            if not request.user is None and request.user.has_role(dev_model.access.get("manage", None)):
                logging.info(str(request.user.id)+": DevicesController:list:command:"+command_alias)
                command_data = dev_model.get_command_by_alias(command_alias)
                if type(command_data) is dict:
                    method_name = command_data.get("command","")
                    if method_name=="devcommand":
                        command_params = command_data.get("command_params",{})
                        if type(command_params) is dict and "command_list" in command_params:
                            BotDevice.run_command(request, command_params["command_list"])    
                            sleep(command_data.get("sleep", 0))
                    elif method_name!="":
                        try:
                            method = getattr(dev_model, method_name, None)
                            if callable(method):
                                # Вызываем метод с переданными аргументами
                                method(command_data.get("command_params"))
                                sleep(command_data.get("sleep", 0))
                                # Проапдейтим сообщение из которого нажимали кнопку
                                dev_update_txt = dev_model.get_info_message("mini")
                                self.message.edit_message_text(request.message.from_user["id"], 
                                                            message_id=request.message.message_id, 
                                                            new_text=dev_update_txt,
                                                            reply_markup=self.message.get_blank_markup_dict(mklist=request.message.reply_markup)) 
                            else:
                                logging.warning(str(request.user.id) + f": Error: DevicesController: Not callable method {method_name} in {dev_model.__class__.__name__}")        
                        except Exception:       
                            logging.exception(str(request.user.id) + f": Error: DevicesController: Method {method_name} in {dev_model.__class__.__name__}")

                    
        else:    
            for dev_alias, device in request.bot.devices.items():
                if not device.get("videocam", False) and not request.user is None and request.user.has_role("user"):
                    dev_model = BotDevice(request.bot, request.bot.devices, dev_alias)
                    if not request.user is None and request.user.has_role(dev_model.access.get("view", None)) \
                        and dev_model.in_location(location_alias):
                        mess_txt = dev_model.get_info_message("mini")
                        if type(dev_model.commands) is dict:
                                line = None
                                all_markup_list = []
                                markup_list = []
                                for command_alias, command_data in dev_model.commands.items():
                                    if type(command_data) is dict:
                                        if line is None:
                                            line = command_data.get("line", 0)    
                                        elif not line is None and line != command_data.get("line", 0): 
                                            if len(markup_list)>0:
                                                all_markup_list.append(markup_list)  
                                            markup_list = []
                                            line = command_data.get("line", 0)
                                        markup_list.append({"text":command_data.get("name",""), 
                                                        "command": request.route_str + ":command:" + dev_alias + ":" + command_alias})   
                        if len(markup_list)>0:
                            all_markup_list.append(markup_list)                                
                        self.message.send(request.chatid, text=mess_txt, reply_markup=self.message.get_blank_markup_dict(mklist=all_markup_list))  

    def change_location(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:change_location")      
 
        command = request.message.command
        location_alias = request.message.command_obj
        location_info = request.message.command_info    

        if request.is_script_command and command=="location":   
            location = BotLocation(request, location_alias)
            logging.info(str(request.user.id)+": Set location: " + location_alias + " to " + location.alias) 
            request.session.set({"location": location.alias,
                                 "route": request.bot.def_route,
                                 "pgnom": 0})
            mess_txt = "Выбрано размещение: " + location.name
            self.message.send(request.chatid, text=mess_txt)
        else:    
            location_alias = request.session.get("location", "")
            location = BotLocation(request, location_alias)
            mess_txt = "Текущее: " + location.name
            all_markup_list = [{"text":"Все", "command":request.route_str+":location:all"}]
            self.message.send(request.chatid, text=mess_txt, reply_markup=self.message.get_blank_markup_dict(mklist=all_markup_list))
            cnt = 1
            for vi1, item1 in request.bot.locations.items():
                if not request.user is None and request.user.has_role(item1.get("access",{}).get("view", None)):
                    mess_txt = "Группа " + str(cnt)
                    all_markup_list = [[{"text": item1["name"], "command":request.route_str+":location:"+vi1}]]
                    items_list = []
                    if "list" in item1:
                        for vi2, item2 in item1["list"].items():
                            if not request.user is None and request.user.has_role(item2.get("access",{}).get("view", None)):
                                items_list.append({"text": item2["name"], "command":request.route_str+":location:"+vi1+"-"+vi2})      
                        if len(items_list)>0:
                            all_markup_list.append(items_list)    
                    self.message.send(request.chatid, text=mess_txt, reply_markup=self.message.get_blank_markup_dict(mklist=all_markup_list))                          
                    cnt += 1

    def view_settings(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:view_settings")
        devices_config = request.bot.conf_obj.get_config("devices")
        mess_txt = json.dumps(devices_config, indent=4)
        self.message.send(request.chatid, text=mess_txt)    

    def dnload_user_settings(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:dnload_user_settings")
        devices_config = request.bot.conf_obj.get_config("devices")
        out_path = request.bot.config["system"].get("out_path", "tmp/out")
        out_file = out_path + "/devices" + str(request.user.id) + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".json"
        try:
            with open(out_file, 'w', encoding='utf-8') as file:   
                json.dump(devices_config, file, ensure_ascii=False, indent=4)  
            with open(out_file, 'rb') as file:
                self.message.send_document(request.chatid, img_buf=file) 
            os.remove(out_file)       
        except Exception:
            logging.exception(str(request.user.id) + ": Error: DevicesController:dnload_user_settings:send_document")

    def upload_user_settings(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:upload_user_settings")
        if request.same_route:
            pass
        elif request.is_script_command: 
            in_path = request.bot.config["system"].get("out_path", "tmp/out")
            in_file = in_path + "/in" + str(request.user.id) + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".bin"
            upload_file_name = self.message.download_file(request.message, in_file)
            logging.info(str(request.user.id)+": DevicesController:upload_user_settings:upload_file_name:"+str(upload_file_name))
            success = False
            if not upload_file_name is None:   
                try:
                    with open(upload_file_name, 'r', encoding='utf-8') as file:
                        config_data = json.load(file)    
                        if type(config_data) is dict:
                            success = request.bot.conf_obj.save_config(config_data, "devices") 
                except Exception:
                    logging.exception(str(request.user.id) + ": Error: DevicesController:upload_user_settings:save_config")
                os.remove(upload_file_name)  
            if success:
                mess_txt = "Конфиг devices успешно загружен!"
                request.bot.reload_configs()
            else:
                mess_txt = "Ошибка загрузки конфига devices.json!"    
            self.message.send(request.chatid, text=mess_txt)     
        else:
            mess_txt = "Поместите сюда файл с конфигом устройств в формате .json"    
            self.message.send(request.chatid, text=mess_txt)


    def del_user_settings(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:del_user_settings") 
        if request.session.get("del_config_waiting_for_input", False):
            request.session.set({"del_config_waiting_for_input": False})
            if request.message.text.lower()=="yes":
                request.bot.conf_obj.delete_config("devices") 
                request.bot.reload_configs()
                mess_txt = f"Пользовательский конфиг devices.json удален"
            else:
                mess_txt = f"Ошибка удаления пользовательского конфига devices.json"  
            self.message.send(request.chatid, text=mess_txt)    
        else:
            mess_txt = "Наберите \"Yes\" для подтверждения удаления пользовательского конфига devices.json"    
            self.message.send(request.chatid, text=mess_txt)
            request.session.set({"del_config_waiting_for_input": True})

    def reload_user_settings(self, request:Request):
        logging.info(str(request.user.id)+": DevicesController:reload_user_settings")
        if request.session.get("reload_config_waiting_for_input", False):
            request.session.set({"reload_config_waiting_for_input": False})
            if request.message.text.lower()=="yes":
                request.bot.reload_configs()
                mess_txt = f"Настройки перезагружены"
            else:
                mess_txt = f"Ошибка удаления перезагрузки настроек"  
            self.message.send(request.chatid, text=mess_txt)    
        else:
            mess_txt = "Наберите \"Yes\" для подтверждения перезагрузки настроек"    
            self.message.send(request.chatid, text=mess_txt)
            request.session.set({"reload_config_waiting_for_input": True})        

    