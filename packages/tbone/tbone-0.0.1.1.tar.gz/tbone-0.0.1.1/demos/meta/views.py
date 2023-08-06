#!/usr/bin/env python
# encoding: utf-8


import json
from aiohttp import web
from models import *

async def Index(request):

    cursor = IMEIQuery.get_cursor(db=request.app.db, query={'imei': '353608060220467'})
    cursor.skip(0)
    cursor.limit(10)
    object_list = await IMEIQuery.find(cursor)

    import pdb; pdb.set_trace()
    return web.Response(text='Hello World')
