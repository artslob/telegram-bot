import asyncio

import aiohttp
from aiohttp import web

import config
from telegram import commands
from telegram.methods import SendMessageMethod, SetWebhookMethod
from telegram.objects import Update


def webhook_address():
    return f'/{config.TOKEN}'


async def register_webhook():
    data = {
        'url': f'{config.HOST}{webhook_address()}',
    }

    for _ in range(config.WEBHOOK_RETRIES):
        try:
            async with SetWebhookMethod.post_json(data) as response:
                if response.status != 200:
                    continue
                result = await response.json()
                if result['ok']:
                    return True
        except aiohttp.client_exceptions.ClientError:
            pass
    return False


async def webhook(request):
    default_response = web.Response()

    update = Update.from_dict(await request.json())
    if not update.message:
        # ignore all messages except direct from users
        return default_response
    message = {
        'chat_id': update.message.chat.id,
        'text': commands.execute_command(update.message.text),
    }
    try:
        async with SendMessageMethod.post_json(message):
            pass
    finally:
        return default_response


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
