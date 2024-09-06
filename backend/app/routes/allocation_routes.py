import falcon
import json
import logging
from app.services.allocation_service import allocate_orders

logger = logging.getLogger(__name__)


class AllocationResource:
    def on_post(self, req, resp):
        try:
            allocate_orders()
            resp.body = json.dumps({'message': 'Allocation completed successfully.'})
            resp.status = falcon.HTTP_200
            logger.info("Order allocation completed successfully.")
        except Exception as e:
            logger.error(f"Error during allocation: {e}")
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': 'Internal Server Error'})


allocation_resource = AllocationResource()
