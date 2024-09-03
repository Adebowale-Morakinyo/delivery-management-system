from peewee import *

db = PostgresqlDatabase(
    'delivery_management_system',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432
)


class BaseModel(Model):
    class Meta:
        database = db
