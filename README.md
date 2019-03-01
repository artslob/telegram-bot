# Telegram bot
Это простой бот для телеграмма.  
Особенности:
1. написан на python3.6 с асинхронной обработкой запросов ([aiohttp](https://aiohttp.readthedocs.io/en/stable/));
2. redis в качестве базы данных;
3. использует [webhook](https://core.telegram.org/bots/api#setwebhook) для получения обновлений;
4. контейнеризация с помощью Docker.

## Тестирование
Для запуска тестов необходимо установить [docker-compose](https://docs.docker.com/compose/install/).
```bash
cd <project dir>
docker-compose -f docker/compose-test.yml up --build --abort-on-container-exit --exit-code-from python-bot-test
```
Либо использовать удалённый интерпретатор python в PyCharm IDE, как описано в **Разработке**.

## Разработка
Для того, чтобы разрабатывать бота на локальной машине, Вам понадобится vps с доступом к нему по ssh.
Предполагается, что на сервере запущен какой-либо веб-сервер (например, apache или nginx) с настроенным TLS.  
Например, для nginx виртуальный сервер будет выглядеть так:
```
server {
    listen 443 http2 ssl;
    listen [::]:443 http2 ssl;

    server_name <bot domain>.<your domain>.tld;

    location / {
        proxy_pass http://127.0.0.1:8081;
    }
}
```
После необходимо пробросить порты через ssh:  
```ssh -f -N -R 8081:localhost:8081 vps```

И запустить бота на локальной машине:  
```docker-compose -f docker/compose-dev.yml up --build```  

Вместо запуска через консоль, удобнее всего добавить удалённый интерпретатор python в PyCharm IDE:
[инструкция](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html).  
Для запуска тестов и разработки понадобятся 2 разных интерпретатора: тесты используют `docker/compose-test.yml`,
разработка использует `docker/compose-dev.yml`.

Если телеграмм заблокирован в Вашей стране, возможно понадобится vpn
([например](https://github.com/Nyr/openvpn-install/)).
