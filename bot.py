import aiohttp
from aiohttp import web

import config


async def root(request):
    data = await request.json()
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': data['message']['text'],
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
    app = web.Application()
    app.add_routes([
        web.post('/', root),
    ])
    web.run_app(app, host='0.0.0.0', port=8081)


if __name__ == '__main__':
    main()
