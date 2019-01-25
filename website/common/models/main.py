from peewee import *

from config import Config
from datetime import datetime

from playhouse.shortcuts import model_to_dict, dict_to_model, update_model_from_dict

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


    @classmethod
    def create_from_dict(cls, data):
        d = cls.create(**data)
        d.save()
        return d


class Article(BaseModel):
    link        = CharField(primary_key=True)
    title       = CharField(default='')
    date        = DateField(default='0000-00-00')
    content     = TextField(default='')
    thumbnail   = CharField(default='')
    tags        = CharField(default='')
    description = CharField(default='')
    category    = CharField(default='')
    updated     = DateField(default='000-00-00')


    @classmethod
    def get_category(cls, category='all'):
        if category == 'all': return cls.select()
        return cls.select().where(cls.category == category)


    @classmethod
    def get_article(cls, link):
        return cls.get_or_none(cls.link == link)


    @classmethod
    def get_latest(cls):
        return cls.select().order_by(cls.date.desc()).get()


    def get_prev_next(self):
        p = n = None

        previous_articles = Article.select().where(Article.date < self.date).order_by(Article.date)
        next_articles     = Article.select().where(Article.date > self.date).order_by(Article.date.desc())

        for i in previous_articles: p = i
        for i in next_articles:     n = i

        return p, n


    class Meta:
        table_name = 'Articles'
