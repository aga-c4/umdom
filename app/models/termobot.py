import requests
import logging

from lang.russian import lang
from agaunibot.sysbf import SysBf

class Termobot:
    url = ''
    auth = None
    requests_ttl = 5

    def __init__(self, *, params={}, config={}):
        if not type(params) is dict:
            params = {}
        self.url = params.get("url", "")
        auth = params.get("webauth", None)
        if type(auth) is dict and "login" in auth and "password" in auth:
            self.auth = (auth["login"], auth["password"])
        if type(config) is dict:
            self.config = config   
        self.requests_ttl = self.config.get("system",{}).get("requests_ttl", self.requests_ttl)     

    def get_info(self):
        req_headers = {}
        req_params = {}
        temperature = None
        try:
            response = requests.get(self.url+'/read', params=req_params, headers=req_headers, auth=self.auth, timeout=self.requests_ttl)
            if response.status_code == 200:
                temperature = float(SysBf.get_substring(str(response.text), "","Â°C"))
        except:
            logging.warning("Error get : " + self.url+'/read:')    
           
        return {"temperature": temperature}
    
    def get_info_str(self, mode:str='full'):
        result = ""
        info = self.get_info()
        if not info.get("temperature") is None:
            metric_str = lang["termobot"].get("temperature", "temperature")
            result += metric_str + ": " + str(info.get("temperature")) + "\n"   
        return result
    
    def set(self, params):
        return False
    
    
