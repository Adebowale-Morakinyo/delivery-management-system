import os
from peewee import *
from app.models.warehouse import Warehouse
from app.models.agent import Agent
from app.models.order import Order

db = PostgresqlDatabase(
    os.getenv('PGDATABASE', 'delivery_management_system'),
    user=os.getenv('PGUSER', 'postgres'),
    password=os.getenv('PGPASSWORD', 'postgres'),
    host=os.getenv('PGHOST', 'localhost'),
    port=int(os.getenv('PGPORT', 5432))
)


def create_tables():
    with db:
        db.create_tables([Warehouse, Agent, Order])
