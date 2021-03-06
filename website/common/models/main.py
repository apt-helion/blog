from common.database import DATABASE
from peewee import CharField, DateField, TextField, Model
from playhouse.shortcuts import model_to_dict


class BaseModel(Model):

    class Meta:
        database = DATABASE

    @classmethod
    def create_from_dict(cls, data):
        d = cls.create(**data)
        d.save()

        return d


class Article(BaseModel):
    link = CharField(primary_key=True)
    title = CharField(default='')
    date = DateField(default='1970-01-01')
    content = TextField(default='')
    thumbnail = CharField(default='')
    tags = CharField(default='')
    description = CharField(default='')
    category = CharField(default='')
    updated = DateField(default='1970-01-01')

    @classmethod
    def get_category(cls, category='all'):
        if category == 'all' or category == 'archive': return cls.select()
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
        next_articles = Article.select().where(Article.date > self.date).order_by(Article.date.desc())

        for i in previous_articles: p = i
        for i in next_articles: n = i

        return p, n

    class Meta:
        table_name = 'Articles'
