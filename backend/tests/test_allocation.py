import unittest
from app.services.allocation_service import haversine_distance, allocate_orders, calculate_payment
from app.models.warehouse import Warehouse
from app.models.agent import Agent
from app.models.order import Order
from peewee import SqliteDatabase


class TestAllocation(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.test_db = SqliteDatabase(':memory:')
        self.test_db.bind([Warehouse, Agent, Order], bind_refs=False, bind_backrefs=False)
        self.test_db.connect()
        self.test_db.create_tables([Warehouse, Agent, Order])

    def tearDown(self):
        self.test_db.drop_tables([Warehouse, Agent, Order])
        self.test_db.close()

    def test_haversine_distance(self):
        # Test the distance calculation
        distance = haversine_distance(0, 0, 1, 1)
        self.assertAlmostEqual(distance, 157.2, places=1)

    def test_allocate_orders(self):
        # Create test data
        warehouse = Warehouse.create(name='Test Warehouse', latitude=0, longitude=0)
        agent = Agent.create(name='Test Agent', warehouse=warehouse, check_in_time='2023-01-01 08:00:00')
        Order.create(warehouse=warehouse, delivery_address='Test Address', latitude=0.1, longitude=0.1)
        Order.create(warehouse=warehouse, delivery_address='Test Address 2', latitude=0.2, longitude=0.2)

        # Run allocation
        allocate_orders()

        # Check results
        self.assertEqual(Order.select().where(Order.status == 'allocated').count(), 2)
        self.assertEqual(agent.total_orders, 2)

    def test_calculate_payment(self):
        agent = Agent(total_orders=30)
        self.assertEqual(calculate_payment(agent), 1050)  # 30 * 35

        agent.total_orders = 60
        self.assertEqual(calculate_payment(agent), 2)
