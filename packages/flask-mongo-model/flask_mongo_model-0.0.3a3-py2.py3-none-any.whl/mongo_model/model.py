# -*- coding: utf-8 -*-


import six
from datetime import datetime
from .connection import conn
from .fields import MongoField, ObjectIDField


class ModelBase(object):
    """Model base class. The design idea is for a particular row
    in the database, there will be only one instance initiated in
    the app context. Any update or delete operations should be done
    through this instance.
    """
    _collection_name = None
    _fields = None
    _inserted = False
    _pk_name = '_id'

    _id = ObjectIDField()

    def __init__(self, *args, **kwargs):
        # initiate _fields in __init__. Note that mutable objects
        # as default value for a variable will sometimes bring up
        # tricky issues.
        # Format of MONGODB_SETTINGS dictionary should be:
        # {
        #     'host': '127.0.0.1',
        #     'port': 27017,
        #     'document_class': dict,
        #     'tz_aware': False,
        #     'connect': True
        # }
        # For detailed explanation, refer to
        # https://api.mongodb.com/python/current/api/pymongo/mongo_client.html
        self._fields = {}
        self._init_fields(kwargs)

    def _init_fields(self, init_dict):
        self._id = init_dict.pop('_id', None)

        for name in dir(self):
            field = super(ModelBase, self).__getattribute__(name)
            if isinstance(field, MongoField):
                if field.required and name not in init_dict:
                    raise ValueError('Required field %s is not provided.' % name)
                self._fields[name] = field
                # Set field values
                if name in init_dict:
                    setattr(self, name, init_dict[name])

    def to_dict(self, for_json=False):
        """generate a dictionary for JSON dump or MongoDB usage."""
        result = {}

        for name, field in six.iteritems(self._fields):
            if isinstance(field.value, datetime) and for_json:
                result[name] = field.value.isoformat()
            elif name != '_id':
                result[name] = field.value

        return result

    def save(self):
        """A method that checks changed fields and save them into
        database or create a new record."""
        if self._id is not None:
            # MongoDB object id not None, instance is created from database record.
            return self._update()
        else:
            return self._create()

    def _update(self):
        """Update object to database"""
        to_update = {}
        for name, field in six.iteritems(self._fields):
            if field.updated and field.mutable:
                to_update[name] = field.value
        result = (conn[self.get_collection_name()]
                  .find_one_and_update({self.get_pk_name(): self.get_pk_value()},
                                       {'$set': to_update}))
        # If no document matched, result will be None.
        if result is not None:
            # update succeed
            succeed = True
            # reset updated flag
            for name in to_update:
                super(ModelBase, self).__getattribute__(name).updated = False
        else:
            # Update failed
            succeed = False

        return succeed

    def _create(self):
        """Create this object in database"""
        result = conn[self.get_collection_name()].insert_one(self.to_dict())
        if result.acknowledged:
            self._id = result.inserted_id
            return True
        else:
            return False

    @classmethod
    def all(cls):
        """Return all the model objects.
        """
        return [cls(**document) for document in conn[cls.get_collection_name()].find()]

    @classmethod
    def get(cls, *args, **kwargs):
        """Get one document from database with kwargs and return an
        model instance.
        """
        document = conn[cls.get_collection_name()].find_one(kwargs)
        # MongoDB will return a null result but not None object.
        return cls(**document) if document else None

    @classmethod
    def delete(cls, *args, **kwargs):
        result = conn[cls.get_collection_name()].delete_many(kwargs)
        return result.deleted_count > 0

    @classmethod
    def get_collection_name(cls):
        return cls._collection_name

    @classmethod
    def get_pk_name(cls):
        return cls._pk_name

    def get_pk_value(self):
        if self.get_pk_name() is None:
            raise ValueError('_pk_name of model %s is not set, please indicate '
                             'before you can get the value of primary key.' % self.__class__.__name__)
        return getattr(self, self.get_pk_name())

    def __setattr__(self, item, value):
        try:
            field = super(ModelBase, self).__getattribute__(item)
        except AttributeError:
            # The attribute is not set yet, skip the check and
            # set it with __setattr__ in super class
            pass
        else:
            if isinstance(field, MongoField):
                field.value = value
                # Field found, do not set it with value, otherwise
                # the MongoField instance will be overwritten.
                return

            # If field is not an instance of MongoField, just
            # set it like normal attributes.

        super(ModelBase, self).__setattr__(item, value)

    def __getattribute__(self, item):
        field = super(ModelBase, self).__getattribute__(item)
        if isinstance(field, MongoField):
            return field.value

        return field

    def populate_fields(self, fields):
        for name in fields:
            if name in self._fields:
                setattr(self, name, fields[name])
