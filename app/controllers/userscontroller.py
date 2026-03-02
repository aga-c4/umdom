import logging

from agaunibot.botapp import app
from agaunibot.request import Request
from agaunibot.user import User

class UsersController:

    def __init__(self):
        self.message = app.message
    
    def list(self, request:Request):
        logging.info(str(request.user.id)+": UserController:list")

        if request.is_script_command and request.message.command=="setrole":

            role = str(request.message.command_obj).lower()
            user_id = str(request.message.command_info)
            user = User(request.bot.conf_obj, user_id)

            if user.has_role(role, "all"):
                user.del_role(role)
            else:
                user.add_role(role)        

            # Проапдейтим сообщение из которого нажимали кнопку
            userdata = user.data
            print("userdata:", user_id)
            print(userdata)

            username = userdata.get("params", {}).get("username","")
            first_name = userdata.get("params", {}).get("first_name","")
            last_name = userdata.get("params", {}).get("last_name","")
            language_code = userdata.get("params", {}).get("language_code","")
            is_bot = userdata.get("params", {}).get("is_bot", False)
            
            mess_txt = "id: " + user_id
            if is_bot:
                mess_txt += " (BOT)"
            mess_txt += " "+language_code+"\n"
            mess_txt += "username: " + username + "\n"   
            mess_txt += "first_name: " + first_name + "\n"
            if last_name!="":
                mess_txt += "last_name: " + last_name + "\n"   
            mess_txt += "roles: " + ", ".join(userdata["roles"]) + "\n"

            markup_list = []
            roles = []
            for role in request.bot.config["system"]["allow_roles"]:
                roles.append({"text":role, "command":request.route_str+":setrole:"+role+":"+user_id})
            if len(roles)>0:
                markup_list.append(roles)    
            markup_list.append({"text":"Удалить", "command":request.route_str+":delete:user:"+user_id})                        
            self.message.edit_message_text(request.message.from_user["id"], 
                                        message_id=request.message.message_id, 
                                        new_text=mess_txt,
                                        reply_markup=self.message.get_blank_markup_dict(mklist=markup_list))                         
        elif request.is_script_command and request.message.command=="delete" and request.message.command_obj=="user":
            user_id = str(request.message.command_info)
            user = User(request.bot.conf_obj, user_id)
            username = user.get("username","")
            mess_txt = f"Наберите \"Yes\" для подтверждения удаления пользователя {username} c Id:{user.id}"    
            self.message.send(request.chatid, text=mess_txt)
            request.session.set({"del_user_waiting_for_input": user.id})
        elif request.session.get("del_user_waiting_for_input", False)!=False:  
            user_id = request.session.get("del_user_waiting_for_input",0)  
            user = User(request.bot.conf_obj, user_id)  
            username = user.get("username","")  
            request.session.set({"del_user_waiting_for_input": False})
            mess_txt = f"Ошибка удаления пользователя {username} c Id:{user.id}"  
            if request.message.text.lower()=="yes":
                if user.delete_user():
                    mess_txt = f"Пользователь {username} c Id:{user.id} удален"
                    request.bot.reload_configs()
                else:
                    mess_txt = f"Ошибка удаления пользователя {username} c Id:{user.id}"      
            self.message.send(request.chatid, text=mess_txt)    
        else:   
            serv_user = User(request.bot.conf_obj, 0) 
            users_reestr = serv_user.get_users()
            for user_id, userdata in users_reestr.items():
                if not "params" in userdata or not type(userdata["params"]) is dict:
                    userdata["params"] = {}
                if not "roles" in userdata or not type(userdata["roles"]) is list:
                    userdata["roles"] = []       
                user_info = self.message.get_user_info(user_id)
                if not user_info is None:
                    userdata["params"] = {**userdata["params"], **user_info}           
                
                username = userdata.get("params", {}).get("username","")
                first_name = userdata.get("params", {}).get("first_name","")
                last_name = userdata.get("params", {}).get("last_name","")
                language_code = userdata.get("params", {}).get("language_code","")
                is_bot = userdata.get("params", {}).get("is_bot", False)

                mess_txt = "id: " + user_id
                if is_bot:
                    mess_txt += " (BOT)"
                mess_txt += " "+language_code+"\n"
                mess_txt += "username: " + username + "\n"   
                mess_txt += "first_name: " + first_name + "\n"
                if last_name!="":
                    mess_txt += "last_name: " + last_name + "\n"   
                mess_txt += "roles: " + ", ".join(userdata["roles"]) + "\n"
                
                all_markup_list = []
                roles = []
                for role in request.bot.config["system"]["allow_roles"]:
                    roles.append({"text":role, "command":request.route_str+":setrole:"+role+":"+str(user_id)})              
                if len(roles)>0:
                    all_markup_list.append(roles)               
                all_markup_list.append([{"text":"Удалить", "command":request.route_str+":delete:user:"+str(user_id)}])   
                self.message.send(request.chatid, text=mess_txt, reply_markup=self.message.get_blank_markup_dict(mklist=all_markup_list))  


    def add_user(self, request:Request):
        logging.info(str(request.user.id)+": UserController:add_user")
        
        if request.session.get("add_user_waiting_for_input", False):
            request.session.set({"add_user_waiting_for_input": False})
            user_id = str(int(request.message.text))
            serv_user = User(request.bot.conf_obj, user_id)
            if serv_user.update_user():
                mess_txt = f"Пользователь {user_id} добавлен"
            else:
                mess_txt = f"Ошибка добавления пользователя {user_id}"  
            self.message.send(request.chatid, text=mess_txt)    
        else:
            mess_txt = "Введите идентификатор пользователя: "
            self.message.send(request.chatid, text=mess_txt)
            request.session.set({"add_user_waiting_for_input": True})
            




    