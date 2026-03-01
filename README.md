**Бот умного дома**
---
**Для запуска:**
1. Копируем или делаем по аналогии sample в корень проекта, поправляем конфиги, скрипты запуска и остальное. 
Папки user нужны для размещения своих контроллеров, моделей и конфигов. Структура и наполнение папки sample
дает общее понимание о возможностях кастомизации и конфигурации бота.
2. Создаем виртуальное окружение и загружаем пакеты в него
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
3. Припишите телеграм идентификатор админа в config.system.telegram_admin_ids в конфигурации main.py в папке user/кастом
4. Пропишите параметры доступа к боту и каналу в config.telegram  в конфигурации main.py в папке user/кастом
5. Запуск бота осуществляется скриптом bot.sh или запуском python3 bot.py
```
python3 bot.py start --custom demo --log_level INFO
```
6. Можно запустить бота под Docker, для этого из корня выполните
```
docker-compose up
```

**Элементы управления ботом**
Файлы бота находятся в папке app. Есть возможность использовать разные конфиги для работы бота. Какой код бота будет использован определяется параметром bot_controllers_prefix и bot_models_prefix конфига main.py из папки конфигов запускаемого бота. Какой конфиг будет использован при запуске определяется параметром custom, позволяющим делать несколько вариантов одного конфига для бота.

Конфиги бота находятся в папке app/configs. Default конфиг определяет все основные параметры и переопределяется custom конфигом.

Дерево общения бота задается конфигом botstru.py, где описываются ноды этого общения, контроллеры,
экшены и параметры их вызова, доступы.

В конфигах есть файл devices.py, он нужен для организации работы ботов, управляющих устройствами. 
Этот файл может не использоваться.

Есть авторизованные и неавторизованные пользователи. Авторизованный пользователи - те, у которых есть сессия 
и статус авторизованности. Эти 2 типа пользователей имеют разные ветки в структуре бота. 
Управление регистрацией и авторизацией ведется на уроне бота, обычно чем-то вроде методов registration и authorization в app/controllers/botcontroller.py, запуск которых регулируется в структуре бота app/configs/default/botstru.py

Можно пользоваться кнопками навигации бота, писать сообщения и вводить данные. Бот может анализировать
входящий текст и отвечать, для примера наберите "тест" в авторизованном и не авторизованном состоянии.

Анализатор текстов можно подключить в конфиге в секции "bot" (analyse_text_controller), посмотрите как это сделано в демо конфиге.


**Всякое полезное**

Ассинхронный бот:
https://www.pvsm.ru/python/373024?ysclid=m8x3pp5r9z484916280
https://docs-python.ru/packages/biblioteka-python-telegram-bot-python/perekhod-versiiu-20/ 
https://s5.hpc.name/thread/t580/76186/ispolzovanie-potokov-i-asinhronnosti-dlya-bota-v-telegram-na-python.html

Мажордомо
https://www.youtube.com/watch?v=4O-2dJwRQtg

Статья про зигби
https://www.youtube.com/watch?v=cyxcQS441tc 
https://habr.com/ru/articles/854878/ 
https://alice.yandex.ru/support/ru/smart-home/how-work/zigbee
https://habr.com/ru/articles/503494/ (шлюзы - разработки)

Zigbee2MQTT
https://www.zigbee2mqtt.io/guide/getting-started/#onboarding
https://www.zigbee2mqtt.io/guide/adapters/emberznet.html
https://www.zigbee2mqtt.io/supported-devices/#v=SONOFF

Работаем с Zigbee-устройствами через Zigbee2mqtt и Node-RED
https://habr.com/ru/companies/wirenboard/articles/713274/ 

MQTT
https://habr.com/ru/articles/463669/
https://pikabu.ru/story/besplatnyiy_i_lichnyiy_mqtt_broker_mosquitto_dlya_iotustroystv_na_bazeubuntu_2004_na_always_free_vps_serverot_oracle_7982336 

ESP8266 MQTT client using pubsubclient library and mosquitto MQTT broker
https://rutube.ru/video/33307e9b0bc103195bd0f5a63263eb08/
Фласк:
https://habr.com/ru/articles/346306/


Передача видео с IP-камер D-Link !!!!!!!!
http://flance.onego.ru/2008/05/22/13


Telegram bot API - разбор документации с примерами
https://infostart.ru/1c/articles/1217332/


Делаем сервисы для бота и автозапуск 
Под рутом:
1. Добавляем в /etc/systemd/system/umdombot.service
сервисы бота, брокера, монитора из папки systemd
2. Устанавливаем права для запуска 
```
chmod 755 /etc/systemd/system/umdombot.service
```
3. Рестартим демон
```
systemctl daemon-reload
```
4. Включаем и активируем автозагрузку сервисов по схеме
```
systemctl start umdombot
systemctl status umdombot
systemctl enable umdombot  (включить сервис)
systemctl disable umdombot  (выключить сервис)
```