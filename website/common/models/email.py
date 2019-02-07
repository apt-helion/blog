import datetime
import uuid

from peewee import *
from common.models.main import BaseModel


class Emails(BaseModel):
    email       = CharField(column_name='email', primary_key=True)
    unsubscribe = CharField(column_name='unsubscribe')
    created     = DateField(column_name='created')

    class Meta:
        table_name = 'Emails'


class EmailLogs(BaseModel):
    id      = AutoField(column_name='id')
    error   = CharField(column_name='error')
    email   = CharField(column_name='email')
    process = CharField(column_name='process')
    date    = DateField(column_name='date')

    class Meta:
        table_name = 'EmailLogs'


class EmailVerifications(BaseModel):
    code   = CharField(column_name='code', primary_key=True)
    email  = CharField(column_name='email')
    expiry = DateTimeField(column_name='expiry')


    @classmethod
    def create_verification(cls, email):
        now = datetime.datetime.now()
        expiry = now + datetime.timedelta(minutes = 30)

        verify = cls.create(
            code = uuid.uuid4().hex,
            email = email,
            expiry = expiry
        )

        return verify


    class Meta:
        table_name = 'EmailVerifications'
