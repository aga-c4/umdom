from agaunibot.request import Request

class BotLocation:

    alias = "all"
    name = "Все размещения"

    def __init__(self, request:Request, location_alias:str):
        if location_alias.strip()!="":
            locations = request.bot.locations
            location_in = location_alias.split('-')        
            for loc_alias1, loc_data1 in locations.items():
                if len(location_in)>0 and location_in[0].strip()!="" and location_in[0]==loc_alias1:
                    if not request.user is None and request.user.has_role(loc_data1.get("access",{}).get("view", None)):
                        self.alias = location_in[0]
                        self.name = loc_data1.get(_("name"), "")
                        if "list" in loc_data1 and type(loc_data1["list"]) is dict \
                            and len(location_in)>1 and location_in[1].strip()!="" \
                            and location_in[1] in loc_data1["list"] \
                            and type(loc_data1["list"][location_in[1]]) is dict:
                                loc_data2 = loc_data1["list"].get(location_in[1])
                                if not request.user is None and request.user.has_role(loc_data2.get("access",{}).get("view", None)):
                                    self.alias += "-" + str(location_in[1])
                                    self.name = loc_data2.get(_("name"), "")
