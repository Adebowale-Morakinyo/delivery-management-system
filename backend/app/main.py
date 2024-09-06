import falcon
from falcon_cors import CORS
import logging
from app.routes.warehouse_routes import warehouse_resource
from app.routes.agent_routes import agent_resource
from app.routes.order_routes import order_resource
from app.routes.allocation_routes import allocation_resource
from app.routes.allocation_routes import metrics_resource

from app.database import db
from app.populate_db import populate_sample_data
from app.models.warehouse import Warehouse
from app.models.agent import Agent
from app.models.order import Order

from config import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Enable CORS
cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
app = falcon.App(middleware=[cors.middleware])


# Create tables if they don't exist
def create_tables():
    with db:
        db.create_tables([Warehouse, Agent, Order])


# app = falcon.App()

logger.info("Starting the application")
# create_tables()
# populate_sample_data()

app.add_route('/warehouses', warehouse_resource)
app.add_route('/agents', agent_resource)
app.add_route('/orders', order_resource)
app.add_route('/allocate', allocation_resource)
app.add_route('/metrics', metrics_resource)


from apscheduler.schedulers.background import BackgroundScheduler
from app.services.allocation_service import allocate_orders

scheduler = BackgroundScheduler()
scheduler.add_job(allocate_orders, 'cron', hour=8, minute=0)
scheduler.start()

"""
if __name__ == '__main__':
    from wsgiref import simple_server
    logger.info("Serving on 0.0.0.0:8000")
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
"""
