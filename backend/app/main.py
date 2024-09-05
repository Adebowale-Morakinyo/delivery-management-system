import falcon
import logging
from app.routes.warehouse_routes import warehouse_resource
from app.routes.agent_routes import agent_resource
from app.routes.order_routes import order_resource
from app.database import db
from app.models.warehouse import Warehouse
from app.models.agent import Agent
from app.models.order import Order

from config import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)


# Create tables if they don't exist
def create_tables():
    with db:
        db.create_tables([Warehouse, Agent, Order])


app = falcon.App()

logger.info("Starting the application")

app.add_route('/warehouses', warehouse_resource)
app.add_route('/agents', agent_resource)
app.add_route('/orders', order_resource)

if __name__ == "__main__":
    create_tables()

"""
if __name__ == '__main__':
    from wsgiref import simple_server
    logger.info("Serving on 0.0.0.0:8000")
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
"""
