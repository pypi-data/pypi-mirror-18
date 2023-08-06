#!/usr/bin/env python
# encoding: utf-8

from schematics.types import *
from schematics.models import Model
from schematics.contrib.mongo import ObjectIdType
from tbone.models import MongoDBMixin


class BaseModel(MongoDBMixin, Model):
    pass


class Author(BaseModel):
    _id = ObjectIdType()
    first_name = StringType(required=True)
    middle_name = StringType(serialize_when_none=False)
    last_name = StringType(required=True)


class Publisher(BaseModel):
    _id = ObjectIdType()
    name = StringType(required=True)


class Book(BaseModel):
    _id = ObjectIdType()
    title = StringType(required=True)
    publication_date = DateType()
    genre = ListType(StringType())
    author = ObjectIdType()
    publishers = DictType(ObjectIdType)

