import falcon
import json
import logging
from app.models.order import Order
from app.models.agent import Agent
from app.services.allocation_service import haversine_distance
from app.database import db
from datetime import date

logger = logging.getLogger(__name__)


class AllocationDetailsResource:
    def on_get(self, req, resp):
        logger.info("Fetching allocation details")
        try:
            today = date.today()
            with db.atomic():
                allocations = []
                orders = Order.select().where(
                    Order.allocated_date == today,
                    Order.status == 'allocated'
                ).order_by(Order.agent_id)

                for order in orders:
                    agent = order.agent
                    allocations.append({
                        'agentName': agent.name,
                        'orderId': order.id,
                        'estimatedDistance': float(haversine_distance(
                            agent.warehouse.latitude, agent.warehouse.longitude, order.latitude, order.longitude
                        )),
                        'estimatedTime': float(order.estimated_time) if hasattr(order, 'estimated_time') else None,
                        'allocationTimestamp': str(order.allocated_date)
                    })

                resp.body = json.dumps(allocations)
                resp.status = falcon.HTTP_200
                logger.info("Allocation details fetched successfully")
        except Exception as e:
            logger.error(f"Error fetching allocation details: {e}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})


allocation_details_resource = AllocationDetailsResource()
