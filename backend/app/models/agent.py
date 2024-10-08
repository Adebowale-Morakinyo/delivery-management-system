from peewee import *
from app.models.base import BaseModel
from app.models.warehouse import Warehouse


class Agent(BaseModel):
    name = CharField(max_length=100)
    warehouse = ForeignKeyField(Warehouse, backref='agents')
    check_in_time = DateTimeField(null=True)
    total_orders = IntegerField(default=0)
    total_distance = DecimalField(max_digits=10, decimal_places=2, default=0)
    total_time = DecimalField(max_digits=10, decimal_places=2, default=0)
    last_order_latitude = DecimalField(max_digits=10, decimal_places=8, null=True)
    last_order_longitude = DecimalField(max_digits=11, decimal_places=8, null=True)

    class Meta:
        table_name = 'agents'
