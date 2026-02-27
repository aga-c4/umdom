import logging
import json
import paho.mqtt.client as mqtt

from app.lang.russian import lang
from app.models.botсache import BotCache

class ZigbeeDevice:
    alias = ''
    url = ''
    auth = None
    info_mini_list = []
    bcache = None
    config = {}

    def __init__(self, *, params={}, config={}):
        if not type(params) is dict:
            params = {}
        self.alias = params.get("alias", "")
        self.url = params.get("url", "")
        auth = params.get("webauth", None)
        if type(auth) is dict and "login" in auth and "password" in auth:
            self.auth = (auth["login"], auth["password"])
        info_mini_list = params.get("info_mini_list")
        if type(info_mini_list) is list and len(info_mini_list)>0:
            self.info_mini_list = info_mini_list    
        devicecache_conf = config.get("system",{}).get("devicecache", {})
        self.bcache = BotCache(host=devicecache_conf.get("host", "127.0.0.1"),
                  port=devicecache_conf.get("port", 6379), 
                  db=devicecache_conf.get("db", 0))         
        if type(config) is dict:
            self.config = config

    def get_info(self):
        topic = f"zigbee2mqtt/{self.alias}"
        info = self.bcache.get(topic)
        if type(info) is dict:
            updtime = self.bcache.get_updtime(self.alias)
            info["updtime"] = updtime 
        if info is None:
            info={}         
        return info
    
    def get_info_str(self, mode:str='full'):
        result = ""
        info = self.get_info()
        if not type(self.info_mini_list) is list or len(self.info_mini_list)==0:
            mode='full'
        for metric, val in info.items():
            if mode=='full' or metric in self.info_mini_list:
                metric_str = lang["zigbee_metrics"].get(metric, metric)
                result += f"{metric_str}: {val}\n"
        return result   

    def set(self, params, topic_tpl="zigbee2mqtt/{alias}/set"):
        try:
            topic = topic_tpl.format(alias=self.alias)
            params_json = json.dumps(params)
            mqtt_conf = self.config.get("system",{}).get("mqtt", {})
            host=mqtt_conf.get("host","127.0.0.1")
            port=mqtt_conf.get("port",1883)
            username=mqtt_conf.get("username", "")         
            password=mqtt_conf.get("password", "")         
            qos=mqtt_conf.get("qos", 1)         

            try:
                mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
                if username!="" and password!="":
                    mqttc.username_pw_set(username=username, password=password)
                mqttc.connect(host, port, 60)
                mqttc.loop_start()
                mqttc.publish(topic, params_json, qos=qos)
                mqttc.loop_stop()
                logging.info(f"ZigbeeDevice:set:topic:{topic} send {params_json}")
            except:
                logging.error("ZigbeeDevice:set:key:" + str(self.alias) + " No connect to MQTT Broker")

        except:
            logging.error("ZigbeeDevice:set:key:" + str(self.alias))
        return True
    
    def use_pairing_mode(self, params:dict={"time": 254}):
        return self.set(params, topic_tpl="zigbee2mqtt/bridge/request/permit_join")
