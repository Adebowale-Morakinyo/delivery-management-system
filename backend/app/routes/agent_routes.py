import falcon
import json
import logging
from app.models.agent import Agent
from app.models.warehouse import Warehouse
from app.database import db

logger = logging.getLogger(__name__)


class AgentResource:
    def on_get(self, req, resp):
        try:
            logger.debug("Fetching all agents")
            with db.atomic():
                agents = [
                    {
                        'id': a.id,
                        'name': a.name,
                        'warehouse_id': a.warehouse.id,
                        'check_in_time': str(a.check_in_time) if a.check_in_time else None,
                        'total_orders': a.total_orders,
                        'total_distance': float(a.total_distance),
                        'total_time': float(a.total_time)
                    }
                    for a in Agent.select()
                ]
            resp.body = json.dumps(agents)
            resp.status = falcon.HTTP_200
            logger.info(f"Returned {len(agents)} agents")
        except Exception as e:
            logger.error(f"Error fetching agents: {e}")
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):
        try:
            data = json.load(req.stream)
            with db.atomic():
                warehouse = Warehouse.get_by_id(data['warehouse_id'])
                agent = Agent.create(
                    name=data['name'],
                    warehouse=warehouse
                )
            resp.body = json.dumps({
                'id': agent.id,
                'name': agent.name,
                'warehouse_id': agent.warehouse.id
            })
            resp.status = falcon.HTTP_201
            logger.info(f"Agent created with ID: {agent.id}")
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            resp.status = falcon.HTTP_500


agent_resource = AgentResource()
