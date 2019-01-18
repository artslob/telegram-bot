import asyncio
import logging

import aiohttp
from aiohttp import web

import config
import config.log
from telegram import commands
from telegram.methods import SendMessageMethod, SetWebhookMethod
from telegram.objects import Update

logger: logging.Logger


def webhook_address():
    return f'/{config.TOKEN}'


async def register_webhook():
    data = {'url': f'{config.HOST}{webhook_address()}'}

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
    try:
        await _webhook(request)
    except Exception:
        logger.exception('while processing webhook')
    finally:
        return web.Response(status=200)


async def _webhook(request):
    update = Update.from_dict(await request.json())
    if not update.message or not update.message.text:
        return  # ignore all except direct messages from users with text

    chat_id = update.message.chat.id
    name = update.message.chat.username
    text = update.message.text
    logger.info('got message from id: %s, username: %s with text %s', chat_id, name, text)

    message = {
        'chat_id': chat_id,
        'text': commands.execute_command(text),
    }
    async with SendMessageMethod.post_json(message):
        pass


def main():
    # init logging
    global logger
    config.log.init_log()
    logger = logging.getLogger('webhook')

    # register webhook
    loop = asyncio.get_event_loop()
    webhook_registered = loop.run_until_complete(register_webhook())
    if not webhook_registered:
        logger.error('could not register webhook')
        return

    # start app
    app = web.Application()
    app.add_routes([
        web.post(webhook_address(), webhook),
    ])
    logger.info('app started')
    web.run_app(app, host='0.0.0.0', port=config.PORT)


if __name__ == '__main__':
    main()
