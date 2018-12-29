from aiohttp import web


async def root(request):
    data = await request.read()
    return web.Response(text=f"Hello, world\n" + data.decode())


def main():
    app = web.Application()
    app.add_routes([
        web.get('/', root),
        web.post('/', root),
    ])
    web.run_app(app, host='0.0.0.0', port=8081)


if __name__ == '__main__':
    main()
