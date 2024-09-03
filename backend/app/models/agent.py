from peewee import *
from backend.app.database import BaseModel
from backend.app.models.warehouse import Warehouse


class Agent(BaseModel):
    name = CharField(max_length=100)
    warehouse = ForeignKeyField(Warehouse, backref='agents')
    check_in_time = DateTimeField(null=True)
    total_orders = IntegerField(default=0)
    total_distance = DecimalField(max_digits=10, decimal_places=2, default=0)
    total_time = DecimalField(max_digits=10, decimal_places=2, default=0)
