import requests
import logging

from app.lang.russian import lang

class TasmotaSW:
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
        requests_ttl = self.config.get("system",{}).get("requests_ttl", self.requests_ttl)          

    def get_info(self):
        req_headers = {}
        req_params = {}
        state = ""
        try:
            response = requests.get(self.url+'/?m=1', params=req_params, headers=req_headers, auth=self.auth, timeout=self.requests_ttl)
            if response.status_code == 200:        
                if response.text.find(">ON<")>=0:
                    state = "ON"
                else:
                    state = "OFF" 
        except:
            logging.warning("Error get : " + self.url+'/?m=1')
             
        return {"state": state}
    
    def get_info_str(self, mode:str='full'):
        result = ""
        info = self.get_info()
        metric_str = lang["refosssw_metrics"].get("state", "state")
        state = info["state"]
        result += f"{metric_str}: {state}\n"       
        return result
        
    def set(self, params):
        req_headers = {}
        req_params = {}
        
        if not type(params) is dict:
            params = {}

        value = params.get("state", None)
        if value is None:
            return False

        info = self.get_info()
        try:
            if value=="ON":
                if info["state"]!="ON":
                    requests.get(self.url+'/?m=1&o=1', params=req_params, headers=req_headers, auth=self.auth)
                    
                info = self.get_info()
                if info["state"]=="ON":
                    return True 
                else:
                    return False 
            elif value=="OFF":
                if info["state"]!="OFF":
                    requests.get(self.url+'/?m=1&o=1', params=req_params, headers=req_headers, auth=self.auth)
                    
                info = self.get_info()
                if info["state"]=="OFF":
                    return True 
                else:
                    return False     
            else:
                return False      
        except:
            return False      
