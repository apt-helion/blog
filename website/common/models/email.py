from peewee import *
from common.models.main import BaseModel


class Emails(BaseModel):
    id = AutoField(column_name='id')
    email = CharField(column_name='email')
    unsubscribe = CharField(column_name='unsubscribe')
    created = DateField(column_name='created')

    class Meta:
        table_name = 'Emails'


class EmailLogs(BaseModel):
    id = AutoField(column_name='id')
    error = CharField(column_name='error')
    email = CharField(column_name='email')
    process = CharField(column_name='process')
    date = DateField(column_name='date')

    class Meta:
        table_name = 'EmailLogs'


class EmailVerifications(BaseModel):
    id = CharField(column_name='id', primary_key=True)
    email = CharField(column_name='email')
    expiry = DateTimeField(column_name='expiry')

    class Meta:
        table_name = 'EmailVerifications'
