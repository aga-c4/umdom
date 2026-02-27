import requests
import logging

from app.lang.russian import lang

class VcamUni:
    url = ''
    auth = None

    def __init__(self, *, params={}, config={}):
        if not type(params) is dict:
            params = {}
        self.url = params.get("url", "")
        auth = params.get("webauth", None)
        if type(auth) is dict and "login" in auth and "password" in auth:
            self.auth = (auth["login"], auth["password"])
        if type(config) is dict:
            self.config = config    

    def get_info(self):
        req_headers = {}
        req_params = {}
        try:
            response = requests.get(self.url, params=req_params, headers=req_headers, auth=self.auth)
            status = "enable"
            if response.status_code == 200:
                status = "active"
        except:
            logging.error("Error get : " + self.url)
            status = "disable"

        return {"status": status}
    
    def get_info_str(self, mode:str='full'):
        result = ""
        res = self.get_info()
        if res["status"]=="active":
            result += "Камера активна\n"
        else:
            result += "Камера недоступна\n"    
        return result
    
    def get_mjpeg(self, uri, out_file):
        req_headers = {}
        req_params = {}
        try:
            response = requests.get(self.url+uri, params=req_params, headers=req_headers, auth=self.auth)
            out = open(out_file, "wb")
            out.write(response.content)
            out.close()
            if response.status_code != 200:
                return None
        except:
            logging.error("Error get : " + self.url+uri)
            return None  
        
        return out_file
    
    def gouri(self, params=None):
        req_headers = {}
        req_params = {}
        uri = ""
        if type(params) is dict:
            uri = params.get("uri","")
        try:
            response = requests.get(self.url+uri, params=req_params, headers=req_headers, auth=self.auth)
            if response.status_code != 200:
                return False 
        except:
            logging.error("Error gourl : " + self.url+uri)
            return False 
        
        return True
    
    def set(self, params):
        return False
    
    
