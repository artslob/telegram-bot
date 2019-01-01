import asyncio

import aiohttp
from aiohttp import web

import config


def webhook_address():
    return f'/{config.TOKEN}'


async def register_webhook():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'url': f'{config.HOST}{webhook_address()}',
    }
    url = f'{config.API}/setWebhook'
    params = dict(url=url, json=data, headers=headers)

    for _ in range(config.WEBHOOK_RETRIES):
        try:
            async with aiohttp.request('POST', **params) as response:
                if response.status != 200:
                    continue
                result = await response.json()
                if result['ok']:
                    return True
        except aiohttp.client_exceptions.ClientError:
            pass
    return False


async def webhook(request):
    update = await request.json()
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'chat_id': update['message']['chat']['id'],
        'text': update['message']['text'],
    }
    url = f'{config.API}/sendMessage'
    params = dict(url=url, json=message, headers=headers)
    try:
        async with aiohttp.request('POST', **params) as response:
            if response.status == 200:
                return web.Response()
    except aiohttp.client_exceptions.ClientError:
        pass
    return web.Response(status=500)


def main():
    loop = asyncio.get_event_loop()
    webhook_registered = loop.run_until_complete(register_webhook())
    if not webhook_registered:
        print('Could not register webhook')
        return
    app = web.Application()
    app.add_routes([
        web.post(webhook_address(), webhook),
    ])
    web.run_app(app, host='0.0.0.0', port=8081)


if __name__ == '__main__':
    main()
