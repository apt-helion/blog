import datetime
import uuid

from peewee import CharField, DateTimeField, AutoField
from common.models.main import BaseModel


class Emails(BaseModel):
    email = CharField(column_name='email', primary_key=True)
    unsubscribe = CharField(column_name='unsubscribe', default=uuid.uuid4().hex)
    created = DateTimeField(column_name='created', default=datetime.datetime.today())

    class Meta:
        table_name = 'Emails'


class EmailLogs(BaseModel):
    id = AutoField(column_name='id')
    error = CharField(column_name='error')
    email = CharField(column_name='email')
    process = CharField(column_name='process')
    date = DateTimeField(column_name='date', default=datetime.datetime.today())

    class Meta:
        table_name = 'EmailLogs'
