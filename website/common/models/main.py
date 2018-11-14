from datetime import datetime
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

    class Meta:
        database = database


class Article(BaseModel):
    id = AutoField(column_name='id')
    link = CharField(column_name='link')
    title = CharField(column_name='title')
    date = DateField(column_name='date', default=datetime.now().date())
    category = CharField(column_name='category', default='')
    content = TextField(column_name='content', default='')
    thumbnail = CharField(column_name='thumbnail', default='dual-parallax.jpg')
    tags = CharField(column_name='tags', default='')
    wip = CharField(column_name='wip', default='yes')

    @classmethod
    def get_category(cls, category='all'):
        if category == 'all':
            return cls.select().where(cls.wip == 'no')
        return cls.select().where(cls.category == category, cls.wip == 'no')
    
    @classmethod
    def get_article(cls, link):
        return cls.get_or_none(cls.link == link, cls.wip == 'no')

    class Meta:
        table_name = 'Articles'
