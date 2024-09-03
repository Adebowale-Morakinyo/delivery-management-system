from peewee import *
from backend.app.database import BaseModel


class Warehouse(BaseModel):
    name = CharField(max_length=100)
    latitude = DecimalField(max_digits=10, decimal_places=8)
    longitude = DecimalField(max_digits=11, decimal_places=8)
