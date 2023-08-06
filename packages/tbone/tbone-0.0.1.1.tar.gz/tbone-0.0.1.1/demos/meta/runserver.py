#!/usr/bin/env python
# encoding: utf-8


import logging
import asyncio
from aiohttp.web import Application, run_app
from tbone.db import connect
from tbone.db.models import create_collections
from tbone.middlewares import database
from routes import routes


db_config = {
    'host': '127.0.0.1',
    'port': 27017,
    'name': 'meta',
    'username': '',
    'password': '',
    'extra': '',
    'connection_retries': 5,
    'reconnect_timeout': 2,  # in seconds
}


def init():
    loop = asyncio.get_event_loop()
    app = Application(loop=loop, middlewares=[database])

    # connect to db
    db = connect(**db_config)
    if db:
        setattr(app, 'db', db)

    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    # app.on_startup.append(create_collections)

    return app


def main():
    logging.basicConfig(level=logging.INFO)
    app = init()
    run_app(
        app,
        host='localhost',
        port=7000
    )


if __name__ == "__main__":
    main()
