import logging
import uuid
from agaunibot.sysbf import SysBf
from agaunibot.mybot import MyBot
from agaunibot.request import Request

from app.models.zigbeedevice import ZigbeeDevice

class BotDevice:

    dev_alias = None
    data = {}
    model = None
    access = {}
    out_path = "tmp/out"
    in_path = "tmp/in"
    commands = {}

    def __init__(self, bot:MyBot, devices:dict, dev_alias:str):
        if dev_alias.strip()!="":
            self.out_path = bot.config["system"].get("out_path", "tmp/out")
            self.in_path = bot.config["system"].get("in_path", "tmp/in")
            self.dev_alias = dev_alias
            self.data = devices.get(dev_alias, {})
            self.data["alias"] = dev_alias
            cur_model_name = bot.config["bot"]["bot_models_prefix"] + self.data["model"].lower()
            self.model = SysBf.class_factory(cur_model_name, self.data["model"], params=self.data, config=bot.config)
            self.access = self.data.get("access", {})
            self.commands = self.data.get("commands", {})

    def in_location(self, location_alias:str):        
        if location_alias=="all" or location_alias=="":
            return True
        dev_location = self.data.get("location", "all")
        if dev_location.startswith(location_alias):
            return True
        return False

    def set_mode(self, mode_str:str):
        if self.model is None:
            logging.warning("Device model "+self.data["model"]+" not found!")
            return (False, "Device model "+self.data["model"]+" not found!")
        if not self.data.get("sw", False):
            logging.warning("Device model "+self.data["model"]+" is not SW!")
            return (False, "Device model "+self.data["model"]+" is not SW!")

        mode = mode_str.lower()
        if mode=="on":
            if self.model.set("ON"):
                return (True, "Успешно включено")
            else:
                logging.warning(f"Device {self.dev_alias} set ON error!")
                return (False, f"Device {self.dev_alias} set ON error!") 
        if mode=="off":
            if self.model.set("OFF"):
                return (True, "Успешно выключено")
            else:
                logging.warning(f"Device {self.dev_alias} set OFF error!")
                return (False, f"Device {self.dev_alias} set OFF error!")     
              
        logging.warning(f"Command {mode_str} error!")      
        return (False, f"Command {mode_str} error!")
    
    def get_info_message(self, mode:str='full'):
        mess_txt = "[ "+self.data.get("name", str(self.dev_alias)) + " ]\n"
        mess_txt += self.model.get_info_str(mode)
        return mess_txt
    
    def get_mjpeg(self, uri):   
        if self.model is None:
            logging.warning("Device model "+self.data["model"]+" not found!")
            return (False, "Device model "+self.data["model"]+" not found!")
        if not self.data.get("videocam", False):
            logging.warning("Device model "+self.data["model"]+" is not videocam!")
            return (False, "Device model "+self.data["model"]+" is not videocam!")

        out_file = self.out_path + "/img-" + str(uuid.uuid4()) + ".jpg"     
        return self.model.get_mjpeg(uri, out_file)

    def use_pairing_mode(self):
        zbdev = ZigbeeDevice()
        return zbdev.use_pairing_mode()
    
    def get(self, key:str, defval=None):
        return self.data.get(key, defval)
    
    def set(self, params):
        return self.model.set(params)
    
    def get_command_by_alias(self, alias):
        data = self.commands.get(alias, None)
        if data is None:
            return data
        result = {
            "alias": alias,
            "name": data.get("name", ""),
            "command": data.get("command", ""),
            "command_params": data.get("command_params",{}),
            "sleep": data.get("sleep", 0)
        }
        return result

    def gouri(self, uri):
        if hasattr(self.model, "gouri"):
            return self.model.gouri(uri)
        else:
            return False
        
    def gourl(self, url):
        if hasattr(self.model, "gourl"):
            return self.model.gourl(url)
        else:
            return False    

    @staticmethod
    def run_command(request:Request, command_list):
        if type(command_list) is str:
            command_list = [command_list]
        if not type(command_list) is list:
            return 0
        
        cnt = 0
        for command_list_item in command_list:
            command_list_item_lst = command_list_item.split(":")    
            if len(command_list_item_lst)>1:
                с_dev_alias = command_list_item_lst[0]
                с_dev_command = command_list_item_lst[1]
                с_value_alias = None
                с_value = None
                if len(command_list_item_lst)>2:
                    с_value_alias = command_list_item_lst[2]
                if len(command_list_item_lst)>3:
                    с_value = command_list_item_lst[3]
                    
                c_device = None
                if с_dev_alias in request.bot.devices:
                    c_device = request.bot.devices[с_dev_alias]
                    c_dev_model = BotDevice(request.bot, request.bot.devices, с_dev_alias)

                if c_device == None:
                    continue

                logging.info(str(request.user.id)+": BotDevice:run_command:"+str(command_list_item))
                c_command_data = c_dev_model.get_command_by_alias(с_dev_command)
                if type(c_command_data) is dict:
                    с_dev_method_name = c_command_data.get("command","")
                    c_command_params = c_command_data.get("command_params",{})
                    if not type(c_command_params) is dict: c_command_params = {}
                    if not с_value_alias is None:
                            c_command_params[с_value_alias] = с_value
                    try:
                        method = getattr(c_dev_model, с_dev_method_name, None)
                        if callable(method):
                            # Вызываем метод с переданными аргументами
                            method(c_command_params)
                            cnt += 1
                        else:
                            logging.warning(str(request.user.id) + f": Error: BotDevice:run_command: Not callable method {с_dev_command} in {c_dev_model.__class__.__name__}")        
                    except:       
                        logging.warning(str(request.user.id) + f": Error: BotDevice:run_command: Method {с_dev_command} in {c_dev_model.__class__.__name__}")
        return cnt