from datetime import datetime
from flask import current_app as app


class ModelBase(object):
    """Model base class. The design idea is for a particular row
    in the database, there will be only one instance initiated in
    the app context. Any update or delete operations should be done
    through this instance.
    """
    _collection_name = None
    _fields = None
    _inserted = False
    _pk_name = None

    def __init__(self, *args, **kwargs):
        # initiate _fields in __init__. Note that mutable objects
        # as default value for a variable will sometimes bring up
        # tricky issues.
        self._fields = {}

    def to_dict(self, for_json=False):
        """generate a dictionary for JSON dump or MongoDB usage."""
        result = {}

        for field in self._fields:
            val = self._get_field_value(field)
            if isinstance(val, datetime) and for_json:
                result[field] = val.isoformat()
            elif field != '_id':
                result[field] = val

        return result

    def save(self):
        """A method that checks changed fields and save them into
        database or create a new record."""
        if self._id is not None:
            # MongoDB object id not None, instance is created from database record.
            return self._update()
        else:
            return self._create()

    def _set_default_value(self, field_name):
        # set the default value
        if callable(self._fields[field_name]['value']):
            # read value from callable for the field
            self._set_field_value(field_name, self._fields[field_name]['value']())
        elif self._fields[field_name]['value'] is None:
            # field value not set, set the default value to field
            if callable(self._fields[field_name]['default']):
                self._set_field_value(field_name, self._fields[field_name]['default']())
            else:
                self._set_field_value(field_name, self._fields[field_name]['default'])

    def _update(self):
        """Update this object to database"""
        self._before_update()
        to_update = {}
        for field in self._fields:
            if self._fields[field]['updated'] and self._fields[field]['mutable']:
                to_update[field] = self._get_field_value(field)
                self._set_default_value(field)
        result = (app.db[self._collection_name]
                  .find_one_and_update({self._pk_name: self.get_pk_value()},
                                       {'$set': to_update}))
        # if no document matched, result will be None.
        # That means update failed.
        if result is not None:
            # update succeed
            succeed = True
            # reset updated status
            for field in to_update:
                self._set_field_updated(field, updated=False)
        else:
            # update failed
            succeed = False
            # reset the fields to its original status

        return succeed

    def _create(self):
        """Create this object in database"""
        self._before_create()
        for field in self._fields:
            self._set_default_value(field)
        result = app.db[self._collection_name].insert_one(self.to_dict())
        if result.acknowledged:
            self._id = result.inserted_id
            self._set_field_updated('_id', updated=False)
            return True
        else:
            return False

    @classmethod
    def all(cls):
        """Return all the model objects. If global cache is expired,
        fetch them from database again. When fetching from database,
        this method will also rebuild the global cache.
        """
        # reset the cache
        # TODO: change to fetch only if dict expired.
        # TODO: make cache a class instance
        app.model_caches[cls._collection_name] = {}
        for obj in app.db[cls._collection_name].find():
            instance = cls(**obj)
            app.model_caches[cls._collection_name][instance.get_pk_value()] = instance

        return app.model_caches[cls._collection_name].values()

    @classmethod
    def get(cls, *args, **kwargs):
        """Get one document from database with kwargs and return an
        model instance.
        """
        try:
            obj = app.model_caches[cls._collection_name][kwargs[cls._pk_name]]
        except KeyError:
            # machine not found in global dictionary, try to get it
            # from database
            document = app.db[cls._collection_name].find_one(kwargs)
            # MongoDB will return a null result but not None object.
            obj = cls(**document) if document else None
            if obj:
                app.model_caches[cls._collection_name][obj.get_pk_value()] = obj

        return obj

    @classmethod
    def delete(cls, *args, **kwargs):
        result = app.db[cls._collection_name].delete_one(kwargs)

        if result.deleted_count > 0:
            try:
                cls.remove_from_cache(kwargs[cls._pk_name])
            except KeyError:
                cls.all()

            return True
        else:
            return False

    @classmethod
    def remove_from_cache(cls, primary_key):
        try:
            del app.model_caches[cls._collection_name][primary_key]
        except KeyError:
            pass

    @classmethod
    def get_collection_name(cls):
        return cls._collection_name

    @classmethod
    def get_pk_name(cls):
        return cls._pk_name

    def get_pk_value(self):
        if self._pk_name is None:
            raise ValueError('_pk_name of model %s is not set, please indicate '
                             'before you can get the value of primary key.' % self.__class__.__name__)
        return self._get_field_value(self._pk_name)

    def _add_field(self, name, value=None, nullable=True, default=None, mutable=True, primary_key=False,
                   build_index=False, **kwargs):
        self._fields[name] = {
            'nullable': nullable,
            'default': default,
            'updated': False,
            'primary_key': primary_key,
            'value': value if value else default,
            'mutable': mutable,
            'build_index': build_index
        }

    def _before_update(self):
        pass

    def _before_create(self):
        pass

    def _set_field_updated(self, name, updated=True):
        self._fields[name]['updated'] = updated

    def _set_field_value(self, name, value):
        if name in self._fields:
            self._fields[name]['value'] = value
            self._set_field_updated(name)

    def _get_field_value(self, name):
        return self._fields[name]['value']

    def _get_field_default(self, name):
        return self._fields[name]['default']

    def __setattr__(self, key, value):
        if key == '_fields' or key not in self._fields:
            super(ModelBase, self).__setattr__(key, value)
        else:
            self._set_field_value(key, value)

    def __getattribute__(self, item):
        if item == '_fields' or item not in self._fields:
            return super(ModelBase, self).__getattribute__(item)
        else:
            return self._get_field_value(item)

    def populate_fields(self, update_dict):
        for key, val in update_dict.iteritems():
            self._set_field_value(key, val)
