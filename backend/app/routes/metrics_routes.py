import falcon
import json
import logging
from app.models.order import Order
from app.models.agent import Agent
from peewee import fn

logger = logging.getLogger(__name__)


class MetricsResource:
    def on_get(self, req, resp):
        try:
            total_orders = Order.select(fn.COUNT(Order.id)).scalar()
            allocated_orders = Order.select(fn.COUNT(Order.id)).where(Order.status == 'allocated').scalar()
            pending_orders = Order.select(fn.COUNT(Order.id)).where(Order.status == 'pending').scalar()
            active_agents = Agent.select(fn.COUNT(Agent.id)).where(Agent.check_in_time.is_null(False)).scalar()

            average_orders_per_agent = round(allocated_orders / active_agents, 2) if active_agents else 0

            metrics = {
                'totalOrders': total_orders,
                'allocatedOrders': allocated_orders,
                'pendingOrders': pending_orders,
                'activeAgents': active_agents,
                'averageOrdersPerAgent': average_orders_per_agent
            }

            resp.body = json.dumps(metrics)
            resp.status = falcon.HTTP_200
            logger.info("Metrics fetched successfully.")
        except Exception as e:
            logger.error(f"Error fetching metrics: {e}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})


metrics_resource = MetricsResource()
