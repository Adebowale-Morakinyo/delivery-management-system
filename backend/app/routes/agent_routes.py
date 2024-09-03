import falcon
import json
from backend.app.models.agent import Agent
from backend.app.models.warehouse import Warehouse


class AgentResource:
    def on_get(self, req, resp):
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

    def on_post(self, req, resp):
        data = json.load(req.stream)
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


agent_resource = AgentResource()
