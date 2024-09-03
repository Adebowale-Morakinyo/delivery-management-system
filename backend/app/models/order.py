from peewee import *
from backend.app.database import BaseModel
from backend.app.models.warehouse import Warehouse
from backend.app.models.agent import Agent


class Order(BaseModel):
    warehouse = ForeignKeyField(Warehouse, backref='orders')
    delivery_address = CharField(max_length=255)
    latitude = DecimalField(max_digits=10, decimal_places=8)
    longitude = DecimalField(max_digits=11, decimal_places=8)
    status = CharField(max_length=20, default='pending')
    agent = ForeignKeyField(Agent, backref='orders', null=True)
    allocated_date = DateField(null=True)
    completed_time = DateTimeField(null=True)
