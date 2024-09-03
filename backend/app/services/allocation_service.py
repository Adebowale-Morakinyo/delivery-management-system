from app.models.agent import Agent
from app.models.order import Order
from app.models.warehouse import Warehouse
from datetime import date, timedelta
import math
from decimal import Decimal


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def allocate_orders():
    today = date.today()
    warehouses = Warehouse.select()

    for warehouse in warehouses:
        agents = Agent.select().where(Agent.warehouse == warehouse, Agent.check_in_time.is_null(False))
        orders = Order.select().where(Order.warehouse == warehouse, Order.status == 'pending')

        orders = sorted(orders, key=lambda o: haversine_distance(
            warehouse.latitude, warehouse.longitude, o.latitude, o.longitude
        ))

        for agent in agents:
            agent_orders = []
            total_distance = Decimal(0)
            total_time = Decimal(0)  # Use Decimal for total_time

            for order in orders:
                if len(agent_orders) == 0:
                    distance = haversine_distance(
                        warehouse.latitude, warehouse.longitude, order.latitude, order.longitude
                    )
                else:
                    last_order = agent_orders[-1]
                    distance = haversine_distance(
                        last_order.latitude, last_order.longitude, order.latitude, order.longitude
                    )

                time = Decimal(distance * 5 / 60)  # Convert time to Decimal

                if total_distance + distance <= Decimal(100) and total_time + time <= Decimal(10):
                    agent_orders.append(order)
                    total_distance += Decimal(distance)
                    total_time += time
                else:
                    break

            for order in agent_orders:
                order.agent = agent
                order.status = 'allocated'
                order.allocated_date = today
                order.save()

            agent.total_orders += len(agent_orders)
            agent.total_distance += total_distance
            agent.total_time += total_time
            agent.save()

            orders = [o for o in orders if o not in agent_orders]

        for order in orders:
            order.allocated_date = today + timedelta(days=1)
            order.save()


def calculate_payment(agent):
    if agent.total_orders >= 50:
        return max(500, agent.total_orders * 42)
    elif agent.total_orders >= 25:
        return max(500, agent.total_orders * 35)
    else:
        return 500


# Run allocation at a specific time (e.g., 8 AM)
def run_allocation():
    from datetime import datetime
    now = datetime.now()
    if now.hour == 8 and now.minute == 0:
        allocate_orders()
