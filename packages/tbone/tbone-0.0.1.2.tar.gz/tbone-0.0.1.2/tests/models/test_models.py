#!/usr/bin/env python
# encoding: utf-8


from dateutil import parser
from tornado.testing import gen_test
from tbone.testing import BaseTestCase
from .models import *


class ModelTestCase(BaseTestCase):

    def setUp(self):
        super(ModelTestCase, self).setUp()

    def tearDown(self):
        super(ModelTestCase, self).tearDown()

    @gen_test
    def test_create_model_and_save_to_db(self):
        # create author model
        cursor = Author.get_cursor(self.db, {})
        # get current count of Author collection
        before = yield cursor.count()
        author = Author({
            'first_name': 'Herman',
            'last_name': 'Melville'
        })
        yield author.save(db=self.db)
        after = yield cursor.count()
        self.assertEqual(before + 1, after)
        # create book model
        book = Book({
            'title': 'Moby-Dick',
            'publication_date': parser.parse('October 18 1851'),
            'genre': ['Novel', 'adventure' 'fiction', 'epic', 'sea story'],
            'author': author._id
        })
        cursor = Book.get_cursor(self.db, {})
        # get current count of Book collection
        before = yield cursor.count()
        yield book.save(db=self.db)
        after = yield cursor.count()
        self.assertEqual(before + 1, after)
        # fetch all books
        cursor = Book.get_cursor(self.db)
        cursor.limit(1000)
        books = yield Book.find(cursor)
        self.assertEqual(len(books), after)

    @gen_test
    def test_create_model_then_find_and_delete(self):
        # create model and save
        author = Author({
            'first_name': 'Maxim',
            'last_name': 'Gorky'
        })
        self.assertIsNone(author._id)
        yield author.save(db=self.db)
        self.assertIsNotNone(author._id)
        # get object from db after save
        a2 = yield Author.find_one(self.db, {'_id': author._id})
        self.assertIsNotNone(a2)
        # delete object from db
        id = author._id
        result = yield author.delete(self.db)
        self.assertEqual(result['ok'], 1)
        # fail to get object from db
        a3 = yield Author.find_one(self.db, {'_id': id})
        self.assertIsNone(a3)

    @gen_test
    def test_updat_model(self):
        ''' Tests the model's  `modify` capabilities '''
        # create model and save
        author = Author({
            'first_name': 'Thomas',
            'middle_name': 'Lanier',
            'last_name': 'Williams'
        })
        self.assertIsNone(author._id)
        yield author.save(db=self.db)
        self.assertIsNotNone(author._id)
        # get object from db after save
        a2 = yield Author.find_one(self.db, {'_id': author._id})
        self.assertIsNotNone(a2)
        # modify object and update
        author.first_name = 'Tennessee'
        author.middle_name = None
        author.update(db=self.db)
        # fetch from db
        a2 = yield Author.find_one(self.db, {'_id': author._id})
        self.assertIsNotNone(a2)
        # even though the object does not have a middle name, the update doesn't remove the field
        self.assertIsNotNone(a2.middle_name)
        # save the object as a whole, overriding fields
        yield author.save(db=self.db)
        a2 = yield Author.find_one(self.db, {'_id': author._id})
        self.assertIsNotNone(a2)
        self.assertIsNone(a2.middle_name)

    # @gen_test
    # def test_model_update(self):
    #     author = Author({
    #         'first_name': 'John',
    #         'middle_name': 'Ernst',
    #         'last_name': 'Steinbeck'
    #     })

    #     yield author.insert(db=self.db)
    #     self.assertIsNotNone(author._id)




