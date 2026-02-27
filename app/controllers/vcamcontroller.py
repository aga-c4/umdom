import logging
import os
from time import sleep
from agaunibot.request import Request
from agaunibot.message import Message
from agaunibot.sysbf import SysBf

from app.models.botdevice import BotDevice

class VcamController:
    
    route_actions = ["list", "viewcam"] # Доступные для маршрутизации методы контроллера
    rotelist = []

    def __init__(self):
        self.message = Message() 

    def route(self, request:Request):
        """Маршрутизация в рамках контроллера"""
        logging.info(str(request.user.id)+": VcamController:route")

        action = ""
        if request.message_type=="callback":
            self.rotelist = request.bot.get_controller_route_by_str(request.message.data)
            action = SysBf.getitem(self.rotelist, 0, "")
            if action in self.route_actions:
                logging.info(str(request.user.id)+": VcamController:route:"+action)
                getattr(self, action)(request)
        else:        
            logging.info(str(request.user.id)+": VcamController:route:list:def")
            getattr(self, "list")(request)        


    def list(self, request:Request):
        logging.info(str(request.user.id)+": VcamController:list")
        location_alias = request.session.get("location", "")

        if not request.is_script_command:
            for dev_alias, device in request.bot.devices.items():
                if device.get("videocam", False) and not request.user is None and request.user.has_role("user"):
                    dev_model = BotDevice(request.bot, request.bot.devices, dev_alias)
                    if not request.user is None and request.user.has_role(dev_model.access.get("view", None)) \
                        and dev_model.in_location(location_alias):
                        mess_txt = dev_model.get_info_message("mini")
                        self.message.send(request.chatid, text=mess_txt)     

                        if not request.user is None and request.user.has_role(dev_model.access.get("manage", None)):
                            reply_markup=self.message.get_blank_markup_dict(mklist=[[
                                                {"text":"Обновить", "command":request.route_str+":viewcam:"+dev_alias+":refresh"},
                                                {"text":"Сохранить", "command":request.route_str+":viewcam:"+dev_alias+":save"},
                                                {"text":"Открыть", "command":request.route_str+":viewcam:"+dev_alias+":inlineview"}
                                                ]])
                            mjpeg_uri = dev_model.get("mjpeg", None)
                            if not mjpeg_uri is None:
                                mjpeg_file_name = dev_model.get_mjpeg(mjpeg_uri)
                                if not mjpeg_file_name is None:
                                    try:  
                                        with open(mjpeg_file_name, 'rb') as file:   
                                            self.message.send_photo(request.chatid, img_buf=file, reply_markup=reply_markup) 
                                        os.remove(mjpeg_file_name)       
                                    except Exception:
                                        logging.exception(str(request.user.id) + ": Error: VcamController:list:send")    

    def viewcam(self, request:Request):
        logging.info(str(request.user.id)+": VcamController:viewcam")
        dev_alias = SysBf.getitem(self.rotelist, 1, "")
        command = SysBf.getitem(self.rotelist, 2, "")
        device = None
        if dev_alias in request.bot.devices:
            device = request.bot.devices[dev_alias]
            dev_model = BotDevice(request.bot, request.bot.devices, dev_alias)

        if device == None or not request.user.has_role(dev_model.access.get("view", None)) or not request.is_script_command:
            return

        if command=="inlineview":
            logging.info(str(request.user.id)+": VcamController:viewcam:inlineview")
            mjpeg_uri = dev_model.get("mjpeg", None)
            if not mjpeg_uri is None:
                mjpeg_file_name = dev_model.get_mjpeg(mjpeg_uri)
                if not mjpeg_file_name is None:
                    try:  
                        with open(mjpeg_file_name, 'rb') as file:
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
                                                        "command": request.route_str + ":viewcam:" + dev_alias + ":" + command_alias}) 
                                if len(markup_list)>0:
                                    all_markup_list.append(markup_list)
                                all_markup_list.append([{"text":"Закрыть", "command":request.route_str+":viewcam:"+dev_alias+":close"}])

                                self.message.edit_message_media(request.message.from_user["id"], 
                                                            message_id=request.message.message_id, 
                                                            img_buf=file,
                                                            reply_markup=self.message.get_blank_markup_dict(mklist=all_markup_list))       
                        os.remove(mjpeg_file_name)       
                    except Exception:
                        logging.exception(str(request.user.id) + ": Error: VcamController:viewcam:inlineview:send") 

        elif command=="view":
            logging.info(str(request.user.id)+": VcamController:viewcam:view")
            mess_txt = "[ " + dev_model.get("name", "Камера") + " ]"
            self.message.send(request.chatid, text=mess_txt)  
            mjpeg_uri = dev_model.get("mjpeg", None)
            if not mjpeg_uri is None:
                mjpeg_file_name = dev_model.get_mjpeg(mjpeg_uri)
                if not mjpeg_file_name is None:
                    try:  
                        with open(mjpeg_file_name, 'rb') as file:
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
                                                        "command": request.route_str + ":viewcam:" + dev_alias + ":" + command_alias}) 
                                if len(markup_list)>0:
                                    all_markup_list.append(markup_list)
                                all_markup_list.append([{"text":"Закрыть", "command":request.route_str+":viewcam:"+dev_alias+":close"}])       
                                
                            self.message.send_photo(request.chatid, img_buf=file, reply_markup=self.message.get_blank_markup_dict(mklist=all_markup_list)) 
                        os.remove(mjpeg_file_name)       
                    except Exception:
                        logging.exception(str(request.user.id) + ": Error: VcamController:viewcam:view:send")   
        elif command=="save": 
            logging.info(str(request.user.id)+": VcamController:viewcam:save")   
            mjpeg_uri = dev_model.get("mjpeg", None)
            if not mjpeg_uri is None:
                mjpeg_file_name = dev_model.get_mjpeg(mjpeg_uri)
                if not mjpeg_file_name is None:
                    try:  
                        with open(mjpeg_file_name, 'rb') as file: 
                            self.message.send_photo(request.chatid, img_buf=file)     
                        os.remove(mjpeg_file_name) 
                    except Exception:
                        logging.exception(str(request.user.id) + ": Error: VcamController:viewcam:save")    
            command="refresh"                        
        elif command!="refresh" and command!="close":
            # Все остальные команды обрабатываются универсальным образом
            logging.info(str(request.user.id)+": VcamController:viewcam:command:"+command)
            command_data = dev_model.get_command_by_alias(command)
            if type(command_data) is dict:
                method_name = command_data.get("command","")
                if method_name=="devcommand":
                    command_params = command_data.get("command_params",{})
                    if type(command_params) is dict and "command_list" in command_params:
                        BotDevice.run_command(request, command_params["command_list"])    
                        sleep(command_data.get("sleep", 0))
                        command = "refresh"
                elif method_name!="":
                    try:
                        method = getattr(dev_model, method_name, None)
                        if callable(method):
                            # Вызываем метод с переданными аргументами
                            method(command_data.get("command_params"))
                            sleep(command_data.get("sleep", 0))
                            command="refresh"
                        else:
                            logging.warning(str(request.user.id) + f": Error: VcamController: Not callable method {method_name} in {dev_model.__class__.__name__}")        
                    except Exception:       
                        logging.exception(str(request.user.id) + f": Error: VcamController: Method {method_name} in {dev_model.__class__.__name__}")
        # При необходимости обновим
        if command=="refresh" or command=="close":
            logging.info(str(request.user.id)+": VcamController:viewcam:"+command)
            mjpeg_uri = dev_model.get("mjpeg", None)
            if not mjpeg_uri is None:
                mjpeg_file_name = dev_model.get_mjpeg(mjpeg_uri)
                if not mjpeg_file_name is None:
                    try:  
                        with open(mjpeg_file_name, 'rb') as file:
                            if command=="close":
                                reply_markup = [[{"text":"Обновить", "command":request.route_str+":viewcam:"+dev_alias+":refresh"},
                                                {"text":"Сохранить", "command":request.route_str+":viewcam:"+dev_alias+":save"},
                                                {"text":"Открыть", "command":request.route_str+":viewcam:"+dev_alias+":inlineview"}]]
                            else:  
                                reply_markup = request.message.reply_markup


                            self.message.edit_message_media(request.message.from_user["id"], 
                                                        message_id=request.message.message_id, 
                                                        img_buf=file,
                                                        reply_markup=self.message.get_blank_markup_dict(mklist=reply_markup))
                        os.remove(mjpeg_file_name)     
                    except Exception:
                        logging.exception(str(request.user.id) + ": Error: VcamController:viewcam:refresh")           