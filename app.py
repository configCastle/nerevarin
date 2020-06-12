"""Main module for project."""
import asyncio
import os
import sys

import aiohttp_cors
from aiohttp import web

from constants import standart_port
from routes import init_routes
from utils.db import init_db


def init_app():
    """
    Initialize application and depend module for it.

    Returns:
        app: instance of application
    """
    app = web.Application()

    loop = asyncio.get_event_loop()
    db = loop.run_until_complete(init_db())
    app['db'] = db

    init_routes(app)

    client_uri = os.getenv('CLIENT_URI', '*')
    aiohttp_cors.setup(app, defaults={
        client_uri: aiohttp_cors.ResourceOptions(
            expose_headers='*',
            allow_headers='*',
            allow_credentials=True,
            allow_methods=['POST', 'GET', 'OPTIONS'],
        ),
    })

    return app


def run():
    """Entry point for server."""
    port = os.getenv('PORT', standart_port)

    web.run_app(init_app(), port=port)


if __name__ == '__main__':
    sys.exit(run())
