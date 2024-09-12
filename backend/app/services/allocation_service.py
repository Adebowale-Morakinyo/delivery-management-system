import logging
from app.models.agent import Agent
from app.models.order import Order
from app.models.warehouse import Warehouse
from app.database import db
from datetime import date, timedelta
from decimal import Decimal
import math
from collections import defaultdict

logger = logging.getLogger(__name__)


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
    logger.info("Starting order allocation process")

    with db.atomic():
        # Fetch all warehouses, agents, and orders in bulk
        warehouses = list(Warehouse.select())
        agents = list(Agent.select().where(Agent.check_in_time.is_null(False)))
        orders = list(Order.select().where(Order.status == 'pending'))

        # Group agents and orders by warehouse
        agents_by_warehouse = defaultdict(list)
        orders_by_warehouse = defaultdict(list)

        for agent in agents:
            agents_by_warehouse[agent.warehouse_id].append(agent)

        for order in orders:
            orders_by_warehouse[order.warehouse_id].append(order)

        # Process each warehouse
        for warehouse in warehouses:
            warehouse_agents = agents_by_warehouse.get(warehouse.id, [])
            warehouse_orders = orders_by_warehouse.get(warehouse.id, [])

            logger.info(f"Processing warehouse: {warehouse.id} - {warehouse.name}")
            logger.info(f"Found {len(warehouse_agents)} available agents and {len(warehouse_orders)} pending orders")

            if not warehouse_agents or not warehouse_orders:
                continue

            # Initialize agent metrics
            agent_metrics = {
                agent.id: {'agent': agent, 'total_distance': Decimal(0), 'total_time': Decimal(0), 'orders': []} for
                agent in warehouse_agents}

            # Sort orders by distance from warehouse (optional, can be removed for further optimization)
            warehouse_orders.sort(key=lambda order: haversine_distance(
                warehouse.latitude, warehouse.longitude, order.latitude, order.longitude
            ))

            # Allocate orders
            for order in warehouse_orders:
                best_agent = min(
                    agent_metrics.values(),
                    key=lambda x: (x['total_distance'], x['total_time'])
                )

                # Calculate distance and time for this order
                if best_agent['orders']:
                    last_order = best_agent['orders'][-1]
                    distance = Decimal(haversine_distance(
                        last_order.latitude, last_order.longitude, order.latitude, order.longitude
                    ))
                else:
                    distance = Decimal(haversine_distance(
                        warehouse.latitude, warehouse.longitude, order.latitude, order.longitude
                    ))
                time = Decimal(distance * 5 / 60)  # Assumed time based on distance

                # Check if agent can take this order
                if best_agent['total_distance'] + distance <= Decimal(100) and best_agent[
                    'total_time'] + time <= Decimal(10):
                    logger.info(f"Allocating order {order.id} to agent {best_agent['agent'].id}")

                    # Update order
                    order.agent = best_agent['agent']
                    order.status = 'allocated'
                    order.allocated_date = today
                    order.estimated_time = time
                    order.save()

                    # Update agent metrics
                    best_agent['total_distance'] += distance
                    best_agent['total_time'] += time
                    best_agent['orders'].append(order)
                else:
                    logger.warning(f"Could not allocate order {order.id}")
                    order.allocated_date = today + timedelta(days=1)
                    order.save()

            # Update agents with their final metrics
            for metrics in agent_metrics.values():
                agent = metrics['agent']
                agent.total_orders = len(metrics['orders'])
                agent.total_distance = metrics['total_distance']
                agent.total_time = metrics['total_time']
                if metrics['orders']:
                    last_order = metrics['orders'][-1]
                    agent.last_order_latitude = last_order.latitude
                    agent.last_order_longitude = last_order.longitude
                agent.save()

    logger.info("Order allocation process completed")


def calculate_payment(agent):
    logger.info(f"Calculating payment for agent {agent.id}")
    if agent.total_orders >= 50:
        return max(500, agent.total_orders * 42)
    elif agent.total_orders >= 25:
        return max(500, agent.total_orders * 35)
    else:
        return 500


def run_allocation():
    from datetime import datetime
    now = datetime.now()
    if now.hour == 8 and now.minute == 0:
        logger.info("Running highly optimized order allocation at 8 AM")
        allocate_orders()
