import logging
from app.models.agent import Agent
from app.models.order import Order
from app.models.warehouse import Warehouse
from datetime import date, timedelta
import math
from decimal import Decimal
import heapq
from sklearn.cluster import KMeans
import numpy as np

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
    logger.info(f"Clustering {len(orders)} orders for {num_agents} agents")
    coordinates = np.array([(order.latitude, order.longitude) for order in orders])
    kmeans = KMeans(n_clusters=num_agents)
    kmeans.fit(coordinates)

    clusters = [[] for _ in range(num_agents)]
    for idx, order in enumerate(orders):
        cluster_id = kmeans.labels_[idx]
        clusters[cluster_id].append(order)

    logger.info(f"Orders clustered into {len(clusters)} groups")
    return clusters


def allocate_orders():
    today = date.today()
    logger.info("Starting order allocation process")
    warehouses = Warehouse.select()

    for warehouse in warehouses:
        logger.info(f"Processing warehouse: {warehouse.id} - {warehouse.name}")

        agents = list(Agent.select().where(Agent.warehouse == warehouse, Agent.check_in_time.is_null(False)))
        orders = list(Order.select().where(Order.warehouse == warehouse, Order.status == 'pending'))

        logger.info(f"Found {len(agents)} available agents and {len(orders)} pending orders")

        # Cluster orders to optimize routes
        order_clusters = cluster_orders(orders, len(agents))

        # Initialize a priority queue (min-heap) for agent assignment
        agent_heap = []
        for agent in agents:
            heapq.heappush(agent_heap, (0, 0, agent))  # (total_distance, total_time, agent)

        for cluster in order_clusters:
            cluster.sort(key=lambda o: haversine_distance(
                warehouse.latitude, warehouse.longitude, o.latitude, o.longitude
            ))

            for order in cluster:
                total_distance, total_time, agent = heapq.heappop(agent_heap)

                if agent.total_orders == 0:
                    distance = Decimal(haversine_distance(
                        warehouse.latitude, warehouse.longitude, order.latitude, order.longitude
                    ))
                else:
                    last_order = Order.select().where(Order.agent == agent).order_by(Order.allocated_date.desc()).get()
                    distance = Decimal(haversine_distance(
                        last_order.latitude, last_order.longitude, order.latitude, order.longitude
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
                    agent.total_distance += total_distance
                    agent.total_time += total_time
                    agent.save()

                    # Push the agent back into the heap with updated values
                    heapq.heappush(agent_heap, (total_distance, total_time, agent))
                else:
                    logger.warning(f"Agent {agent.id} reached max capacity for distance/time")
                    heapq.heappush(agent_heap, (total_distance, total_time, agent))
                    break

        # Postpone unallocated orders
        unallocated_orders = [order for cluster in order_clusters for order in cluster if order.status == 'pending']
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
