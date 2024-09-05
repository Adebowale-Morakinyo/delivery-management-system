import falcon
import json
import logging
from app.models.warehouse import Warehouse

# Create a logger instance
logger = logging.getLogger(__name__)


class WarehouseResource:
    def on_get(self, req, resp):
        logger.info("Received GET request for warehouses")
        try:
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
            logger.info(f"Warehouses successfully fetched: {len(warehouses)} warehouses found")
        except Exception as e:
            logger.error(f"Error fetching warehouses: {str(e)}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})

    def on_post(self, req, resp):
        logger.info("Received POST request to create a warehouse")
        try:
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
            logger.info(f"Warehouse created successfully with ID: {warehouse.id}")
        except Exception as e:
            logger.error(f"Error creating warehouse: {str(e)}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})


warehouse_resource = WarehouseResource()
