import datetime
from peewee import *
from config import Config
import math

database = Config.DATABASE


# monkey patch the DateTimeField to add support for the isoformt which is what
# peewee exports as from DataSet
DateTimeField.formats.append('%Y-%m-%dT%H:%M:%S')
DateField.formats.append('%Y-%m-%dT%H:%M:%S')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    # Example usage
    #       doc = AdminDocument.create()
    #       doc.apply(request.form)
    #       doc.apply(request.json)
    #       doc.apply(request.json, required=['filename'], dates=['uploaddate'])
    def apply_request(self, source, ignore = None, required = None, dates = None):

        for field in self._meta.get_sorted_fields():
            data = source.get(field)
            if field == "id": continue
            if field in ignore: continue
            # Verify in required_fields
            if field in required and data == None:
                return {'error': 'Empty required field'}
            if field in dates:
                data = "" # strp==]===
            if data is None or data == "": continue
            self.__dict__[field] = data

        return ""

    class Meta:
        database = database

class Article(BaseModel):
    id = AutoField(column_name='id')
    link = CharField(column_name='link')
    title = CharField(column_name='title')
    date = DateField(column_name='date')
    category = CharField(column_name='category')
    content = TextField(column_name='content')
    thumbnail = CharField(column_name='thumbnail')
    tags = CharField(column_name='tags')
    wip = CharField(column_name='wip')

    @classmethod
    def get_category(cls, category='all'):
        if category == 'all':
            return cls.select().where(cls.wip == 'no')
        return cls.select().where(cls.category == category, cls.wip == 'no')
    
    @classmethod
    def get_article(cls, link):
        return cls.get(cls.link == link, cls.wip == 'no')

    class Meta:
        table_name = 'Articles'
