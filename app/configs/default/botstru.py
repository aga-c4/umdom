class botstru:

    config = {
        "variants": {
            "noauth_ru": {
                "message": "Привет, {name}!",
                "access": {"view": "noroles"},   
                "if_auth_redirect": ["def_node"],
                "variants": {
                    "authorization": {
                        "action": "Авторизация",
                        "message": "Авторизация:",
                        "access": {"view": "noroles"},
                        "if_auth_redirect": ["def_node"],
                        "contoller": "BotController",
                        "contoller_action": "authorization"
                    },
                    "registration": {
                        "action": "Регистрация",
                        "message": "Регистрация:",
                        "access": {"view": "noroles"},
                        "if_auth_redirect": ["def_node"],
                        "contoller": "BotController",
                        "contoller_action": "registration"  
                    },
                    "help": {
                        "action": "Помощь",
                        "message": "Авторизуйтесь или Зарегистрируйтесь для начала работы с системой",
                        "access": {"view": "noroles"},
                        "fast_back": True      
                    }    
                } 
            }, 
            "main_ru": {
                "message": "Главная:",
                "access": {"view": "user"},
                "variants": {
                    "devices": {
                        "action": "Устройства",
                        "message": "Устройства:",
                        "contoller": "DevicesController",
                        "contoller_action": "list",   
                        "access": {"view": "user"},    
                    },
                    "videocams": {
                        "action": "Камеры",
                        "message": "Камеры:",
                        "contoller": "VcamController",
                        "contoller_action": "route",   
                        "access": {"view": "video_view"},    
                    },
                    "settings": {
                        "action": "Настройки",
                        "message": "Настройки:",
                        "access": {"view": "admin"}, 
                        "variants": {
                            "get_info": {
                                "action": "Инфо",
                                "message": "Информация:",
                                "contoller": "DevicesController",
                                "contoller_action": "get_info",   
                                "access": {"view": "user"},
                                "fast_back": True   
                            },
                            "dnload": {
                                "action": "Скачать",
                                "message": "Скачать:",
                                "contoller": "DevicesController",
                                "contoller_action": "dnload_user_settings",    
                                "access": {"view": "admin"}, 
                            },
                            "upload": {
                                "action": "Загрузить",
                                "message": "Загрузить:",
                                "contoller": "DevicesController",
                                "contoller_action": "upload_user_settings",    
                                "access": {"view": "admin"}, 
                            },
                            "delcustom": {
                                "action": "Удалить",
                                "message": "Удалить доп настройки:",
                                "contoller": "DevicesController",
                                "contoller_action": "del_user_settings",
                                "access": {"view": "admin"}, 
                            },
                            "reload": {
                                "action": "Рестарт",
                                "message": "Перезагрузка настроек:",
                                "contoller": "DevicesController",
                                "contoller_action": "reload_user_settings",
                                "access": {"view": "admin"}, 
                            },
                            "users": {
                                "action": "Польз-ли",
                                "message": "Пользователи:",
                                "access": {"view": "admin"}, 
                                "variants": {
                                    "list": {
                                        "action": "Список",
                                        "message": "Список пользователей:",
                                        "contoller": "UsersController",
                                        "contoller_action": "list",    
                                        "access": {"view": "admin"}, 
                                    },
                                    "add_user": {
                                        "action": "Добавить",
                                        "message": "Добавить пользователя:",
                                        "contoller": "UsersController",
                                        "contoller_action": "add_user",    
                                        "access": {"view": "admin"}, 
                                    }
                                }    
                            },
                            "getip": {
                                "action": "IP адрес",
                                "message": "IP адрес бота:",
                                "contoller": "BotController",
                                "contoller_action": "get_ip",    
                                "access": {"view": "admin"},
                                "fast_back": True         
                            },
                            "zigbee_pairing_mode": {
                                "action": "Поиск устройств",
                                "message": "Поиск устройств:",
                                "contoller": "DevicesController",
                                "contoller_action": "zigbee_pairing_mode",    
                                "access": {"view": "admin"}, 
                            },
                        }
                    },
                    "location": {
                                "action": "Размещение",
                                "message": "Размещение:",
                                "contoller": "DevicesController",
                                "contoller_action": "change_location",  
                                "access": {"view": "user"},  
                            },
                }   
            }             
        }
    }    