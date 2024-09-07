import falcon
import json
import logging
from app.models.order import Order
from app.models.warehouse import Warehouse
from app.database import db

# Create a logger instance
logger = logging.getLogger(__name__)


class OrderResource:
    def on_get(self, req, resp):
        logger.info("Received GET request for orders")
        try:
            with db.atomic():
                orders = [
                    {
                        'id': o.id,
                        'warehouse_id': o.warehouse.id,
                        'delivery_address': o.delivery_address,
                        'latitude': float(o.latitude),
                        'longitude': float(o.longitude),
                        'status': o.status,
                        'agent_id': o.agent.id if o.agent else None,
                        'allocated_date': str(o.allocated_date) if o.allocated_date else None,
                        'completed_time': str(o.completed_time) if o.completed_time else None
                    }
                    for o in Order.select()
                ]
            resp.body = json.dumps(orders)
            resp.status = falcon.HTTP_200
            logger.info(f"Orders successfully fetched: {len(orders)} orders found")
        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})

    def on_post(self, req, resp):
        logger.info("Received POST request to create an order")
        try:
            data = json.load(req.stream)
            with db.atomic():
                warehouse = Warehouse.get_by_id(data['warehouse_id'])
                order = Order.create(
                    warehouse=warehouse,
                    delivery_address=data['delivery_address'],
                    latitude=data['latitude'],
                    longitude=data['longitude']
                )
            resp.body = json.dumps({
                'id': order.id,
                'warehouse_id': order.warehouse.id,
                'delivery_address': order.delivery_address,
                'latitude': float(order.latitude),
                'longitude': float(order.longitude),
                'status': order.status
            })
            resp.status = falcon.HTTP_201
            logger.info(f"Order created successfully with ID: {order.id}")
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})


order_resource = OrderResource()
