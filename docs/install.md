**Установка элементов бота умного дома**

Установка Zigbee2MQTT
https://www.zigbee2mqtt.io/guide/installation/01_linux.html#optional-running-as-a-daemon-with-systemctl

```
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install -y nodejs
sudo apt install gcc g++ make -y
npm install -g pnpm
```

Verify that the correct nodejs and pnpm version has been installed
```
node --version  # Should output V20.x, V22.X
pnpm --version  # Should output 10.X
```

для устранения ошибки с сертификатом при установке может помочь:
request to https://registry.npmjs.org/pnpm failed, reason: unable to get local issuer certificate
```
npm config set strict-ssl false
```

Если надо поставить Yarn:
```
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update && sudo apt-get install yarn -y
```

Мой адаптер Zigbee 3.0 Стик SONOFF USB Dongle Plus-E (Координатор)
https://www.zigbee2mqtt.io/guide/adapters/emberznet.html
Конфигурация:
```
serial:
    adapter: ember
```

Устройство подключено к USB порту, я его нахожу командой:
```
lsusb -v
```
в выдаче много всего, среди прочего "Sonoff Zigbee 3.0 USB Dongle Plus V2"
Bus 001 Device 005: ID 10c4:ea60 Silicon Labs CP210x UART Bridge
Это же показывает и команда:
```
lsusb
```

По итогу вытащил, воткнул, выполнил команду:
```
dmesg
```
посмотрел лог, увидел
usb 1-3
В итоге помогла команда:
```
dmesg | grep attached
```
Устройство нашлось тут:
usb 1-3: cp210x converter now attached to ttyUSB0
Итого нашли: /dev/ttyUSB0

На расбери
usb 1-1.4: Product: Sonoff Zigbee 3.0 USB Dongle Plus V2
Итого нашли: /dev/ttyUSB0

Идем на http://localhost:8080/
заполняем начальную конфигурацию, применяем.

Перезапускаем.
В итоге ошибка:
error: 	z2m: Error: Adapter EZSP protocol version (8) is not supported by Host [13-16].

Для запуска Zigbee2MQTT:
```
pnpm start
```
Как настроить запуск сервиса написано тут:
https://www.zigbee2mqtt.io/guide/installation/01_linux.html#optional-running-as-a-daemon-with-systemctl


Походу придется прошивать адаптер
моя прошивка тут:
https://github.com/itead/Sonoff_Zigbee_Dongle_Firmware/blob/master/Dongle-E/NCP_7.4.4/README.md
Для прошивки идем на сайт
https://darkxst.github.io/silabs-firmware-builder/
выбираем свое устройство. подключаемся, выбираем порт. Я просто обновил прошивку, можно свою залить.
Ошибка с EZSP ушла.


Теперь нам надо поставить MQTT брокер. Ставить будем Mosquitto
```
sudo apt install mosquitto mosquitto-clients -y
```
Сразу настроим для  Mosquitto подписку по логину и паролю (пример логина - LOGIN/PASSWORD):
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd LOGIN
```

Связка логин-пароль будет храниться по следующему пути /etc/mosquitto/passwd
Запретим анонимные подключения к Mosquitto. Открываем файл default.conf:
```
sudo nano /etc/mosquitto/conf.d/default.conf
```
Он должен быть пустой, вставляем туда этот текст:
```
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Перезагружаем Mosquitto чтобы применить изменения:
```
sudo systemctl restart mosquitto
```

Для проверки
```
mosquitto_sub -h localhost -t "test" -u "LOGIN" -P "PASSWORD" 
mosquitto_pub -h localhost -t "test" -m "Privet Mosquito!" -u "LOGIN" -P "PASSWORD" 
```

Для включения режима поиска устройств зигби:
https://www.zigbee2mqtt.io/guide/usage/pairing_devices.html#mqtt
```
mosquitto_pub -h localhost -t "zigbee2mqtt/bridge/request/permit_join" -m '{"time": 254}' -u "LOGIN" -P "PASSWORD" 
```

нашло:
```
[2025-04-23 12:08:43] info: 	z2m:mqtt: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"definition":{"description":"Zigbee smart plug","exposes":[{"features":[{"access":7,"description":"On/off state of the switch","label":"State","name":"state","property":"state","type":"binary","value_off":"OFF","value_on":"ON","value_toggle":"TOGGLE"}],"type":"switch"},{"access":1,"category":"diagnostic","description":"Link quality (signal strength)","label":"Linkquality","name":"linkquality","property":"linkquality","type":"numeric","unit":"lqi","value_max":255,"value_min":0}],"model":"S26R2ZB","options":[{"access":2,"description":"State actions will also be published as 'action' when true (default false).","label":"State action","name":"state_action","property":"state_action","type":"binary","value_off":false,"value_on":true}],"supports_ota":false,"vendor":"SONOFF"},"friendly_name":"0x00124b002b4895a0","ieee_address":"0x00124b002b4895a0","status":"successful","supported":true},"type":"device_interview"}'
[2025-04-23 12:08:43] info: 	z2m:mqtt: MQTT publish: topic 'zigbee2mqtt/0x00124b002b4895a0', payload '{"linkquality":184,"state":"OFF"}'
[2025-04-23 12:08:43] info: 	z2m: Successfully configured '0x00124b002b4895a0'
[2025-04-23 12:08:59] info: 	zh:controller: Succesfully interviewed '0xa4c138359de09f0d'
[2025-04-23 12:08:59] info: 	z2m: Successfully interviewed '0xa4c138359de09f0d', device has successfully been paired
[2025-04-23 12:08:59] info: 	z2m: Device '0xa4c138359de09f0d' is supported, identified as: Tuya Luminance motion sensor (ZG-204ZL)
[2025-04-23 12:08:59] info: 	z2m:mqtt: MQTT publish: topic 'zigbee2mqtt/bridge/event', payload '{"data":{"definition":{"description":"Luminance motion sensor","exposes":[{"access":1,"description":"Indicates whether the device detected occupancy","label":"Occupancy","name":"occupancy","property":"occupancy","type":"binary","value_off":false,"value_on":true},{"access":1,"description":"Measured illuminance","label":"Illuminance","name":"illuminance","property":"illuminance","type":"numeric","unit":"lx"},{"access":1,"category":"diagnostic","description":"Remaining battery in %, can take up to 24 hours before reported","label":"Battery","name":"battery","property":"battery","type":"numeric","unit":"%","value_max":100,"value_min":0},{"access":3,"description":"PIR sensor sensitivity (refresh and update only while active)","label":"Sensitivity","name":"sensitivity","property":"sensitivity","type":"enum","values":["low","medium","high"]},{"access":3,"description":"PIR keep time in seconds (refresh and update only while active)","label":"Keep time","name":"keep_time","property":"keep_time","type":"enum","values":["10","30","60","120"]},{"access":3,"description":"Brightness acquisition interval (refresh and update only while active)","label":"Illuminance interval","name":"illuminance_interval","property":"illuminance_interval","type":"numeric","unit":"minutes","value_max":720,"value_min":1,"value_step":1},{"access":1,"category":"diagnostic","description":"Link quality (signal strength)","label":"Linkquality","name":"linkquality","property":"linkquality","type":"numeric","unit":"lqi","value_max":255,"value_min":0}],"model":"ZG-204ZL","options":[{"access":2,"description":"Calibrates the illuminance value (percentual offset), takes into effect on next report of device.","label":"Illuminance calibration","name":"illuminance_calibration","property":"illuminance_calibration","type":"numeric"}],"supports_ota":false,"vendor":"Tuya"},"friendly_name":"0xa4c138359de09f0d","ieee_address":"0xa4c138359de09f0d","status":"successful","supported":true},"type":"device_interview"}'
```

Включение розетки
```
mosquitto_pub -h localhost -t "zigbee2mqtt/sw1/set" -m '{ "state": "ON" }' -u "c"
mosquitto_pub -h localhost -t "zigbee2mqtt/sw1/set" -m '{ "state": "OFF" }' -u "LOGIN" -P "PASSWORD"
mosquitto_pub -h localhost -t "zigbee2mqtt/sw1/set" -m '{ "state": "TOGGLE" }' -u "LOGIN" -P "PASSWORD"
```

Подписка на получение данных с датчика движения:
```
mosquitto_sub -h localhost -t "zigbee2mqtt/motion1" -u "LOGIN" -P "PASSWORD"
```

Запрос данных по состоянию устройства переключателя:
```
mosquitto_pub -h localhost -t "zigbee2mqtt/sw2/get" -m '{ "state": "" }' -u "LOGIN" -P "PASSWORD"
```

Получение всех данных (параметр -v выводит в начале топик, что бывает полезно, если мы подписываемся на группу топиков):
```
mosquitto_sub -h localhost -t "zigbee2mqtt/#" -u "LOGIN" -P "PASSWORD" -v
```

Для того чтобы zigbee2mqtt отправлял статус устройства с флагом "retain" нужно в конфиге zigbee2mqtt в описании устройства добавить:
```
retain: true
```

Получиться что-то вроде:
```
'0x00158d000422fde9':
  friendly_name: '0x00158d000422fde9'
  retain: true
```

В результате брокер сохранит соощение и после перезагрузки оно будет доступно.  Это можно делать для датчиков, по которым важно такое
сохранение состояния. К примеру датчик движения с датчиком освещенности, чтоб после перезагрузки сразу было корректное значение по свету.


Ставим аналог Redis
```
$ echo "deb https://download.keydb.dev/open-source-dist $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/keydb.list
$ sudo wget  --no-check-certificate -O /etc/apt/trusted.gpg.d/keydb.gpg https://download.keydb.dev/open-source-dist/keyring.gpg
$ sudo apt update
$ sudo apt install keydb
```

В проекте Python (только для разработки):
```
pip3 install keydb-python
```
не удалось установить. будем пользоваться
```
pip install redis
```
Для базового функционала по идее должно и так сработать.
Установим клиент для работы с MQTT
```
pip3 install paho-mqtt
```

