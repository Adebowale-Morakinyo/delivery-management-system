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

    class Meta:
        table_name = 'agents'

    # Comparison method for Agent instances
    def __lt__(self, other):
        # Compare based on total_distance first, then total_time
        if self.total_distance == other.total_distance:
            return self.total_time < other.total_time
        return self.total_distance < other.total_distance
