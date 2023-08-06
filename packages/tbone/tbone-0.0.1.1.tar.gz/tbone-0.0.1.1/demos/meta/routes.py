#!/usr/bin/env python
# encoding: utf-8


from tbone.resources.routers import Router
from resources import *
from views import Index

_phone_router = Router(name='api/phone')
_phone_router.register(TACResource, 'tac')
_phone_router.register(IMEIResource, 'imei_query')
_phone_router.register(PhoneModelResource, 'model')

routes = []

routes += _phone_router.urls()

routes += [
    ('GET', '/', Index, 'index'),
]

