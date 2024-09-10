import logging
from app.models.agent import Agent
from app.models.order import Order
from app.models.warehouse import Warehouse
from app.database import db
from datetime import date, timedelta
import math
from decimal import Decimal
from app.data_structures.min_heap import MinHeapNode, MinHeap

# Create a logger instance
logger = logging.getLogger(__name__)


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def cluster_orders(orders, num_agents):
    logger.info(f"Clustering {len(orders)} orders for {num_agents} agents using custom clustering")

    # Define the geographical bounds
    min_lat = min(order.latitude for order in orders)
    max_lat = max(order.latitude for order in orders)
    min_lon = min(order.longitude for order in orders)
    max_lon = max(order.longitude for order in orders)

    # Calculate grid size
    lat_step = (max_lat - min_lat) / num_agents if num_agents > 0 else 0
    lon_step = (max_lon - min_lon) / num_agents if num_agents > 0 else 0

    clusters = [[] for _ in range(num_agents)]

    for order in orders:
        # Determine cluster index based on position
        lat_idx = int((order.latitude - min_lat) / lat_step) if lat_step > 0 else 0
        lon_idx = int((order.longitude - min_lon) / lon_step) if lon_step > 0 else 0
        cluster_idx = (lat_idx + lon_idx) % num_agents  # Simple way to distribute
        clusters[cluster_idx].append(order)

    logger.info(f"Orders clustered into {len(clusters)} groups using custom clustering")
    return clusters


def allocate_orders():
    today = date.today()
    logger.info("Starting order allocation process")
    with db.atomic():
        warehouses = Warehouse.select()

        for warehouse in warehouses:
            logger.info(f"Processing warehouse: {warehouse.id} - {warehouse.name}")

            agents = list(Agent.select().where(
                Agent.warehouse == warehouse,
                Agent.check_in_time.is_null(False)
            ))
            orders = list(Order.select().where(
                Order.warehouse == warehouse,
                Order.status == 'pending'
            ))

            logger.info(f"Found {len(agents)} available agents and {len(orders)} pending orders")

            if not agents or not orders:
                continue

            # Cluster orders using custom clustering
            order_clusters = cluster_orders(orders, len(agents))

            # Initialize custom MinHeap for agents
            agent_heap = MinHeap()
            for agent in agents:
                agent_heap.insert(MinHeapNode(Decimal(0), Decimal(0), agent))

            for idx, cluster in enumerate(order_clusters):
                cluster.sort(key=lambda o: haversine_distance(
                    warehouse.latitude, warehouse.longitude, o.latitude, o.longitude
                ))

                # Get the agent for this cluster
                agent_node = agent_heap.extract_min()
                agent = agent_node.agent
                total_distance = agent_node.total_distance
                total_time = agent_node.total_time

                for order in cluster:
                    distance = Decimal(haversine_distance(
                        warehouse.latitude, warehouse.longitude, order.latitude, order.longitude
                    )) if agent.total_orders == 0 else Decimal(haversine_distance(
                        agent.last_order_latitude, agent.last_order_longitude, order.latitude, order.longitude
                    ))
                    time = Decimal(distance * 5 / 60)

                    if total_distance + distance <= Decimal(100) and total_time + time <= Decimal(10):
                        logger.info(f"Allocating order {order.id} to agent {agent.id}")

                        # Assign the order to the agent
                        order.agent = agent
                        order.status = 'allocated'
                        order.allocated_date = today
                        order.save()

                        # Update agent metrics
                        agent.total_orders += 1
                        total_distance += distance
                        total_time += time
                        agent.total_distance += distance
                        agent.total_time += time

                        # Store last order location for agent
                        agent.last_order_latitude = order.latitude
                        agent.last_order_longitude = order.longitude
                        agent.save()
                    else:
                        logger.warning(f"Agent {agent.id} reached max capacity for distance/time")
                        break  # Move to next agent

                # Re-insert the agent into the heap
                agent_heap.insert(MinHeapNode(total_distance, total_time, agent))

            # Postpone unallocated orders
            unallocated_orders = Order.select().where(
                Order.warehouse == warehouse,
                Order.status == 'pending'
            )
            for order in unallocated_orders:
                logger.info(f"Postponing unallocated order {order.id} to next day")
                order.allocated_date = today + timedelta(days=1)
                order.save()

    logger.info("Order allocation process completed")


def calculate_payment(agent):
    logger.info(f"Calculating payment for agent {agent.id}")
    if agent.total_orders >= 50:
        return max(500, agent.total_orders * 42)
    elif agent.total_orders >= 25:
        return max(500, agent.total_orders * 35)
    else:
        return 500


# Run allocation at a specific time
def run_allocation():
    from datetime import datetime
    now = datetime.now()
    if now.hour == 8 and now.minute == 0:
        logger.info("Running order allocation at 8 AM")
        allocate_orders()
