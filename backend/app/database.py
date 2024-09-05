import os
from peewee import *

db = PostgresqlDatabase(
    os.getenv('PGDATABASE', 'delivery_management_system'),  # default to your dev DB
    user=os.getenv('PGUSER', 'postgres'),
    password=os.getenv('PGPASSWORD', 'postgres'),
    host=os.getenv('PGHOST', 'localhost'),  # Change to 'localhost' for dev, use env for prod
    port=int(os.getenv('PGPORT', 5432))
)


class BaseModel(Model):
    class Meta:
        database = db
