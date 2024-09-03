import falcon
from app.routes.warehouse_routes import warehouse_resource
from app.routes.agent_routes import agent_resource
from app.routes.order_routes import order_resource

app = falcon.App()

app.add_route('/warehouses', warehouse_resource)
app.add_route('/agents', agent_resource)
app.add_route('/orders', order_resource)

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
