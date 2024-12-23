from functools import cache

from aiohttp import web

@cache
def get_app() -> web:
    app = web.Application()
    return app