import unittest
from datetime import datetime
from mongo_model.mongo_model import ModelBase


class TestModel(ModelBase):
    def __init__(self):
        super(TestModel, self).__init__()
        self._add_field('field1')
        self.test_date = datetime.utcnow()
        self._add_field('datetime1', value=self.test_date)
        self._add_field('_id')


class MongoModelTest(unittest.TestCase):
    def test_init(self):
        instance = TestModel()
        # initiate _fields from None to {}
        self.assertIsNotNone(instance._fields)

    def test_to_dict_non_json(self):
        instance = TestModel()
        d = instance.to_dict()
        self.assertIn('field1', d)
        self.assertIn('datetime1', d)
        self.assertIsInstance(d['datetime1'], datetime)
        # should ignore Mongo object _id
        self.assertNotIn('_id', instance.to_dict())

    def test_to_dict_for_json(self):
        instance = TestModel()
        d = instance.to_dict(for_json=True)
        self.assertIn('field1', d)
        self.assertIn('datetime1', d)
        self.assertIsInstance(d['datetime1'], str)
        self.assertEqual(d['datetime1'], instance.test_date.isoformat())
        # should ignore Mongo object _id
        self.assertNotIn('_id', d)
