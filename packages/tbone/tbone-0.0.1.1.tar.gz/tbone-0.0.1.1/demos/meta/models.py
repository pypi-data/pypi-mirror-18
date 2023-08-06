#!/usr/bin/env python
# encoding: utf-8

from pymongo import ASCENDING
from schematics.types import *
from schematics.models import Model
from schematics.contrib.mongo import ObjectIdType
from tbone.db.models import MongoDBMixin
from tbone.db.types import *


class BaseModel(Model, MongoDBMixin):
    _id = ObjectIdType()


class TAC(BaseModel):
    ''' Represents a TAC entry '''
    primary_key = 'tac'
    primary_key_type = int

    tac = IntType(required=True)
    manufacturer = StringType(required=True)
    vendor = StringType(required=True)
    model = StringType(required=True)
    name = StringType()
    os = StringType()
    phone_model = ObjectIdType()
    internal = StringType(serialize_when_none=False)

    class Options:
        namespace = 'phone'

    indices = [
        {
            'fields': [('tac', ASCENDING)],
            'unique': True
        }
    ]


class IMEIQuery(BaseModel):
    '''Represents a single query to a IMEI database. Currently implementing GSMA only'''
    imei = StringType(required=True)
    source = IntType(default=1)
    data = FreeFormDictType()

    class Options:
        namespace = 'phone'

    indices = [
        {
            'fields': [('imei', ASCENDING)]
        }
    ]

    @classmethod
    def validate_imei(cls, num):
        ''' Validate number using the luhn algorithm'''
        if num.isdigit() is False:
            return False

        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]

        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return (checksum % 10) == 0


class PhoneModel(BaseModel):
    ''' Represents a phone model, data provided by manufacturer '''
    brand = StringType(required=True)
    model = StringType(required=True)
    manufacturer = StringType(required=True)
    providers_name = DictType(StringType, default={})
    other_names = ListType(StringType, default=[])
    battery = DictType(StringType, serialize_when_none=False)
    body = DictType(StringType, serialize_when_none=False)
    camera = DictType(StringType, serialize_when_none=False)
    communication = DictType(StringType, serialize_when_none=False)
    display = DictType(StringType, serialize_when_none=False)
    features = DictType(StringType, serialize_when_none=False)
    launch = DictType(StringType, serialize_when_none=False)
    media = DictType(URLType, serialize_when_none=False)
    memory = DictType(StringType, serialize_when_none=False)
    misc = DictType(StringType, serialize_when_none=False)
    network = DictType(StringType, serialize_when_none=False)
    platform = DictType(StringType, serialize_when_none=False)
    sound = DictType(StringType, serialize_when_none=False)

    class Options:
        namespace = 'phone'