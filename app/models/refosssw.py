import logging
import requests
from agaunibot.sysbf import SysBf

from app.lang.russian import lang

class RefossSW:
    url = ''
    auth = None
    info_mini_list = ["temperature", "voltage", "current_i", "active_power", "state"]
    requests_ttl = 5

    def __init__(self, *, params={}, config={}):
        if not type(params) is dict:
            params = {}
        self.url = params.get("url", "")
        auth = params.get("webauth", None)
        if type(auth) is dict and "login" in auth and "password" in auth:
            self.auth = (auth["login"], auth["password"])
        info_mini_list = params.get("info_mini_list")
        if type(info_mini_list) is list and len(info_mini_list)>0:
            self.info_mini_list = info_mini_list    
        if type(config) is dict:
            self.config = config
        requests_ttl = self.config.get("system",{}).get("requests_ttl", self.requests_ttl)                

    def get_info(self):
        req_headers = {}
        req_params = {}
        info = {
            "temperature": None,
            "voltage": None,
            "current_i": None,
            "active_power": None,
            "apparent_power": None,
            "reactive_power": None,
            "power_factor": None,
            "energy_today": None,
            "energy_yesterday": None,
            "energy_total": None,
            "state": None
        }
        try:
            response = requests.get(self.url+'/?m=1', params=req_params, 
                                    headers=req_headers, 
                                    auth=self.auth, 
                                    timeout=self.requests_ttl)
            if response.status_code == 200:
                info = {
                    "temperature": float(SysBf.get_substring(str(response.text), "Temperature{m}"," Â°C{e}")),
                    "voltage": float(SysBf.get_substring(str(response.text), "Voltage{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> V{e}{s}")),
                    "current_i": float(SysBf.get_substring(str(response.text), "{s}Current{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> A{e}{s}")),
                    "active_power": float(SysBf.get_substring(str(response.text), "{s}Active Power{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> W{e}{s}")),
                    "apparent_power": float(SysBf.get_substring(str(response.text), "{e}{s}Apparent Power{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> VA{e}")),
                    "reactive_power": float(SysBf.get_substring(str(response.text), "{s}Reactive Power{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> VAr{e}")), 
                    "power_factor": float(SysBf.get_substring(str(response.text), "{s}Power Factor{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td>{e}{s}Energy Today{m}")),
                    "energy_today": float(SysBf.get_substring(str(response.text), "{s}Energy Today{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> kWh{e}{s}Energy Yesterday{m}")),
                    "energy_yesterday": float(SysBf.get_substring(str(response.text), "{s}Energy Yesterday{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> kWh{e}{s}Energy Total{m}")),
                    "energy_total": float(SysBf.get_substring(str(response.text), "{s}Energy Total{m}</td><td style='text-align:left'>","</td><td>&nbsp;</td><td> kWh{e}</table><hr/>{t}</table>"))
                }
                state = "None"
                if response.text.find(">ON<")>=0:
                    state = "ON"
                else:
                    state = "OFF"
                info["state"] = state  
        except:
            logging.warning("Error get : " + self.url+'/?m=1')      
        return info
    
    def get_info_str(self, mode:str='mini'):
        result = ""
        info = self.get_info()
        for metric, val in info.items():
            if mode=='full' or metric in self.info_mini_list:
                metric_str = lang["refosssw_metrics"].get(metric, metric)
                result += f"{metric_str}: {val}\n"
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
        
