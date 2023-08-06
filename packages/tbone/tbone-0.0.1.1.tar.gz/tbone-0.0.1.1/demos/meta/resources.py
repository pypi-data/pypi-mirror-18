#!/usr/bin/env python
# encoding: utf-8

import json
from aiohttp import ClientSession
from tbone.resources import Resource, MongoResource
from models import *

TAC_SIZE = 8

GSMA_URL = 'https://devicecheck.gsma.com/imeirtl/detailedblwithmodelinfo/'
GSMA_USERNAME = 'amitn'
GSMA_APIKEY = 'C429000041055'

session = ClientSession()


class IMEIResource(Resource):

    object_class = IMEIQuery
    pk = 'imei'

    async def detail(self, **kwargs):
        imei = kwargs['pk']
        # validate input
        if IMEIQuery.validate_imei(imei):

            limit = int(kwargs.get('limit', self.limit))
            offset = int(kwargs.get('offset', self.offset))
            cursor = self.object_class.get_cursor(self.db, {'imei': imei})
            cursor.skip(offset)
            cursor.limit(limit)
            object_list = await self.object_class.find(cursor)
            if len(object_list) == 0:
                # fetch from gsma
                # create http client
                res = await session.post(
                    url=GSMA_URL,
                    data={
                        'imeinumber': imei,
                        'username': GSMA_USERNAME,
                        'apikey': GSMA_APIKEY
                    },
                    headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                )
                # if res.error:
                #     # do your thing
                #     pass

                body = await res.text()
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                data = json.loads(body)
                obj = IMEIQuery({
                    'imei': data.pop('IMEI'),
                    'source': 1,  # gsma
                    'data': data
                })
                await obj.insert(db=self.db)
            else:
                # TODO: pick the latest one
                obj = object_list[0]

            # get or create TAC object
            tac = int(imei[:TAC_SIZE])
            tac_obj = await TAC.find_one(self.db, {'tac': tac})
            if tac_obj is None:
                tac_obj = TAC(raw_data={
                    'tac': tac,
                    'vendor': obj['data']['brandname'],
                    'manufacturer': obj['data']['manufacturer'],
                    'model': obj['data']['modelname'],
                    'name': obj['data']['marketingname']
                })
                await tac_obj.save(self.db)
            return {
                'imei': obj.imei,
                'data': obj.data
            }
        else:
            raise BadRequest('Invalid IMEI')


class TACResource(MongoResource):
    object_class = TAC


class PhoneModelResource(MongoResource):
    object_class = PhoneModel

