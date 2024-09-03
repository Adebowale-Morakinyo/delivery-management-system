import falcon
import json
from backend.app.models.order import Order
from backend.app.models.warehouse import Warehouse


class OrderResource:
    def on_get(self, req, resp):
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

    def on_post(self, req, resp):
        data = json.load(req.stream)
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


order_resource = OrderResource()
