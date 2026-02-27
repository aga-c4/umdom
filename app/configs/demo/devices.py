# Конфигурация подключенных устройств. Авторежимы настраиваются через бота.
# Очередность определяет порядок вывода информации и порядок кнопок управления.
class devices:

    config = {
        "locations": {
            "home": {
                "name": "Дом",
                "access": {"view": "user"},
                "list": {
                    "flow1": {
                        "name": "Этаж-1",
                        "access": {"view": "user"},
                    },
                    "flow2": {
                        "name": "Этаж-2",
                        "access": {"view": "user"},
                    }
                }
            },
            "ogorod": {
                "name": "Улица",
                "access": {"view": "user"},
            },
        },
        "devices": {
            "Yard_LT": {
                "name": "Двор свет SW",
                "model": "ZigbeeDevice",
                "info_mini_list": ["state","voltage"],
                "send": True,
                "auto_mode": True,
                "access": {"view": "user", "manage":"manage", "update":"admin"}, 
                "location": "ogorod",
                "vals": {"state"},
                "commands": {
                    "on": {
                        "line": 1,
                        "name": "Вкл",
                        "command": "set",
                        "command_params": {"state": "ON"},
                        "sleep": 0.3
                    },
                    "off": {
                        "line": 1,
                        "name": "Выкл",
                        "command": "set",
                        "command_params": {"state": "OFF"},
                        "sleep": 0.3
                    },
                }    
            },
            "Yard_Motion": {
                "name": "Гост. Движ",
                "model": "ZigbeeDevice",
                "info_mini_list": ["battery", "illuminance", "occupancy", "sensitivity"],
                "send": True,
                "auto_mode": False,
                "save_log": True,
                "access": {"view": "user"},
                "location": "ogorod",
                "vals": ["illuminance"]
            },
            "Main_Vhod_LT": {
                "name": "Осн. Вход LT",
                "model": "ZigbeeDevice",
                "info_mini_list": ["state_left", "state_right"],
                "send": True,
                "auto_mode": True,
                "access": {"view": "user", "manage":"manage", "update":"admin"}, 
                "location": "home-flow1",
                "vals": ["state_right"],
                "commands": {
                    "on": {
                        "line": 1,
                        "name": "Вкл",
                        "command": "set",
                        "command_params": {"state_right": "ON", "state_left": "ON"},
                        "sleep": 0.3
                    },
                    "off": {
                        "line": 1,
                        "name": "Выкл",
                        "command": "set",
                        "command_params": {"state_right": "OFF", "state_left": "OFF"},
                        "sleep": 0.3
                    }
                }
            },
            "Yard_T": {
                "name": "Улица Т",
                "model": "ZigbeeDevice",
                "info_mini_list": ["battery", "temperature","humidity"],
                "send": True,
                "auto_mode": False,
                "save_log": True,
                "access": {"view": "user"},
                "location": "ogorod",
                "vals": ["temperature","humidity"]
            },
            "Main_Bedroom1_T": {
                "name": "Осн. Спальня1 Т",
                "model": "ZigbeeDevice",
                "info_mini_list": ["battery", "temperature","humidity"],
                "send": True,
                "auto_mode": False,
                "save_log": True,
                "access": {"view": "user"},
                "location": "home-flow1",
                "vals": ["temperature","humidity"]
            },
            "termobot4": {
                "name": "Гост. ком1",
                "type": "sensor",
                "model": "Termobot",
                "url": "http://192.168.1.113",
                "send": True,
                "location": "guest-flow1",
                "access": {"view": "user", "manage":"manage", "update":"admin"}, 
                "vals": ["temperature"],
            },
            "tasmota1": {
                "name": "Гост. ком1 SW",
                "model": "TasmotaSW",
                "send": True,
                "auto_mode": True,
                "url": "http://192.168.1.108",
                "access": {"view": "user", "manage":"manage", "update":"admin"}, 
                "location": "guest-flow1",
                "vals": ["state"],
                "commands": {
                    "on": {
                        "line": 1,
                        "name": "Вкл",
                        "command": "set",
                        "command_params": {"state": "ON"}
                    },
                    "off": {
                        "line": 1,
                        "name": "Выкл",
                        "command": "set",
                        "command_params": {"state": "OFF"}
                    },
                }
            },
            "refoss1": {
                "name": "Гост. SW2",
                "model": "RefossSW",
                "url": "http://192.168.1.144",
                "send": True,
                "location": "guest-flow1",
                "access": {"view": "user", "manage":"manage", "update":"admin"}, 
                "auto_mode": True,
                "max_exec_sec": 1 * 60 * 60, # максимальное время работы в сек. 0 - без ограничения
                "vals": ["state"],
                "commands": {
                    "on": {
                        "line": 1,
                        "name": "Вкл",
                        "command": "set",
                        "command_params": {"state": "ON"}
                    },
                    "off": {
                        "line": 1,
                        "name": "Выкл",
                        "command": "set",
                        "command_params": {"state": "OFF"}
                    },
                }
            },
            "vcam1": {
                "name": "Двор",
                "model": "VcamUni",
                "videocam": True,
                "location": "ogorod",
                "access": {"view": "video_view", "manage":"video_manage", "update":"admin"}, 
                "url": "http://192.168.1.86",
                "webauth": {"login": "vuser", "password": "PASSWORD!!!"},
                "mjpeg": "/cgi-bin/video.jpg", # Motion JPEG
                "mjpegsize": [704, 576],
                "commands": {
                    "refresh": {
                        "line": 1,
                        "name": "Обновить",
                        "command": "refresh"
                    },
                    "up": {
                        "line": 1,
                        "name": "Вверх",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?move=up"},
                        "sleep": 1
                    },
                    "save": {
                        "line": 1,
                        "name": "Сохранить",
                        "command": "save"
                    },
                    "left": {
                        "line": 2,
                        "name": "Влево",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?move=left"},
                        "sleep": 1
                    },
                    "home": {
                        "line": 2,
                        "name": "Домой",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?move=home"},
                        "sleep": 2
                    },
                    "right": {
                        "line": 2,
                        "name": "Вправо",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?move=right"},
                        "sleep": 1
                    },
                    "zoomdec": {
                        "line": 3,
                        "name": "z-",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?zoom=wide"},
                        "sleep": 1
                    },
                    "down": {
                        "line": 3,
                        "name": "Вниз",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?move=down"},
                        "sleep": 1
                    },
                    "zoominc": {
                        "line": 3,
                        "name": "z+",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?zoom=tele"},
                        "sleep": 1
                    },
                    "focus": {
                        "line": 4,
                        "name": "Фокус",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/camctrl.cgi?focus=auto"},
                        "sleep": 1
                    },
                    "lighton": {
                        "line": 4,
                        "name": "Свет Вкл",
                        "command": "devcommand",
                        "command_params": {"command_list": ["zgbsw4:on"]},
                        "sleep": 4
                    },
                    "lightoff": {
                        "line": 4,
                        "name": "Свет Выкл",
                        "command": "devcommand",
                        "command_params": {"command_list": ["zgbsw4:off"]},
                        "sleep": 4
                    },
                    "yura": {
                        "line": 6,
                        "name": "Юра",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/recall.cgi?recall=Yura"},
                        "sleep": 2
                    },
                    "car": {
                        "line": 6,
                        "name": "Площадка",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/recall.cgi?recall=car"},
                        "sleep": 2
                    },
                    "dom": {
                        "line": 6,
                        "name": "Дом",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/recall.cgi?recall=Dom"},
                        "sleep": 2
                    },
                    "yura2": {
                        "line": 7,
                        "name": "Юра гараж",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/recall.cgi?recall=yura2"},
                        "sleep": 2
                    },
                    "gostvhod2": {
                        "line": 7,
                        "name": "Гост.Лев",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/recall.cgi?recall=gostvhod2"},
                        "sleep": 2
                    },
                    "gostvhod1": {
                        "line": 7,
                        "name": "Гост.Прав",
                        "command": "gouri",
                        "command_params": {"uri": "/cgi-bin/recall.cgi?recall=gostvhod1"},
                        "sleep": 2
                    }
                }
            },          
        },
        # Настройка авторежима
        # По условию формируются задания в очередь, которая постепенно разбирается и исполняется.
        "auto": [
            {  # Группa команд Гост. свет улица
                "name": "Гост. свет улица",    
                "active": True,
                "starton": ["timer:m30", "motion1"], # timer: m1, m15, m30, h1, h2, h4, h8, h12, d1, w1 
                "source": {
                    "src1": "motion1.occupancy",
                    "src2": "motion1.illuminance",
                },
                "commands": [
                    {
                        "active": True,
                        "comment": "Гост. свет улица дежурный OFF",
                        "command": "zgbsw4:off", # (str|list) Выполняемая команда или список команд
                    },
                    { 
                        "active": True,
                        "comment": "Гост. свет улица",
                        "command": "zgbsw4:on", # (str|list) Выполняемая команда или список команд. Команда может быть sleep.3, тогда будет пауза
                        "conditions": {
                            "exp_if": "(src1==True) and (src2<1000)", # Можно задать логическую формулу с параметрами из source, которая должна дать True 
                            "week": [1,2,3,4,5,6,7],
                            "time": [["20:00","09:00"]]
                        }
                    },
                    {
                        "active": True,
                        "comment": "Гост. свет улица дежурный ON",
                        "command": "zgbsw4:on", # (str|list) Выполняемая команда или список команд
                        "conditions": {
                            "week": [1,2,3,4,5,6,7],
                            "time": [["21:00","01:00"]]
                        }
                    },
                ]    
            }    
        ]
    }    




    """
    "termobot4": {
        "name": "Гост. ком1",
        "type": "sensor",
        "model": "Termobot",
        "url": "http://192.168.1.113",
        "send": True,
        "location": "guest-flow1",
        "access": {"view": "user", "manage":"manage", "update":"admin"}, 
        "vals": ["temperature"],
    },
    "termobot1": {
        "name": "Улица",
        "model": "Termobot",
        "url": "http://192.168.1.103",
        "send": True,
        "save_log": True,
        "access": {"view": "user"},
        "location": "home-flow1",
        "vals": ["temperature"],
    },
    "termobot2": {
        "name": "Осн. сан1",
        "model": "Termobot",
        "url": "http://192.168.1.49",
        "send": True,
        "save_log": True,
        "access": {"view": "user"},
        "location": "home-flow1",
        "vals": ["temperature"],
    },  
    "termobot3": {
        "name": "Термо Контейнер",
        "model": "Termobot",
        "url": "http://192.168.1.83",
        "send": True,
        "access": {"view": "user"},
        "location": "ogorod",
        "vals": ["temperature"],
    }, 
    "tasmota1": {
        "name": "Гост. ком1 SW",
        "model": "TasmotaSW",
        "send": True,
        "auto_mode": True,
        "url": "http://192.168.1.108",
        "access": {"view": "user", "manage":"manage", "update":"admin"}, 
        "location": "guest-flow1",
        "vals": ["state"],
        "commands": {
            "on": {
                "line": 1,
                "name": "Вкл",
                "command": "set",
                "command_params": {"state": "ON"}
            },
            "off": {
                "line": 1,
                "name": "Выкл",
                "command": "set",
                "command_params": {"state": "OFF"}
            },
        }
    },
    "dim1": {
        "name": "Гост. dim1",
        "model": "ZigbeeDevice",
        "info_mini_list": ["state", "brightness"],
        "send": True,
        "auto_mode": True,
        "access": {"view": "user", "manage":"manage", "update":"admin"}, 
        "location": "guest-flow1",
        "vals": {"state"},
        "commands": {
            "on": {
                "line": 1,
                "name": "Вкл",
                "command": "set",
                "command_params": {"state": "ON"},
                "sleep": 0.3
            },
            "off": {
                "line": 1,
                "name": "Выкл",
                "command": "set",
                "command_params": {"state": "OFF"},
                "sleep": 0.3
            },
        }    
    },
    "refoss1": {
        "name": "Гост. SW2",
        "model": "RefossSW",
        "url": "http://192.168.1.144",
        "send": True,
        "location": "guest-flow1",
        "access": {"view": "user", "manage":"manage", "update":"admin"}, 
        "auto_mode": True,
        "max_exec_sec": 1 * 60 * 60, # максимальное время работы в сек. 0 - без ограничения
        "vals": ["state"],
        "commands": {
            "on": {
                "line": 1,
                "name": "Вкл",
                "command": "set",
                "command_params": {"state": "ON"}
            },
            "off": {
                "line": 1,
                "name": "Выкл",
                "command": "set",
                "command_params": {"state": "OFF"}
            },
        }
    },
    """    
