import falcon
import json
from app.models.warehouse import Warehouse


class WarehouseResource:
    def on_get(self, req, resp):
        warehouses = [
            {
                'id': w.id,
                'name': w.name,
                'latitude': float(w.latitude),
                'longitude': float(w.longitude)
            }
            for w in Warehouse.select()
        ]
        resp.body = json.dumps(warehouses)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = json.load(req.stream)
        warehouse = Warehouse.create(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        resp.body = json.dumps({
            'id': warehouse.id,
            'name': warehouse.name,
            'latitude': float(warehouse.latitude),
            'longitude': float(warehouse.longitude)
        })
        resp.status = falcon.HTTP_201


warehouse_resource = WarehouseResource()
