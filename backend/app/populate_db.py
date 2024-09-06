import random
from datetime import datetime

from app.models.warehouse import Warehouse
from app.models.agent import Agent
from app.models.order import Order


def populate_sample_data():
    # Create 10 warehouses
    for i in range(1, 11):
        warehouse = Warehouse.create(
            name=f'Warehouse {i}',
            latitude=random.uniform(40.0, 42.0),  # Random latitudes
            longitude=random.uniform(-75.0, -73.0)  # Random longitudes
        )

        # Create 20 agents per warehouse
        for j in range(1, 21):
            agent = Agent.create(
                name=f'Agent {j} at {warehouse.name}',
                warehouse=warehouse,
                check_in_time=datetime.now()
            )

            # Create 60 orders for each agent
            for k in range(1, 61):
                Order.create(
                    warehouse=warehouse,
                    delivery_address=f'Address {k} for {agent.name}',
                    latitude=random.uniform(40.0, 42.0),
                    longitude=random.uniform(-75.0, -73.0),
                    agent=agent,
                    allocated_date=datetime.now().date()
                )
