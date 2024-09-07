import os
from peewee import *

db = PostgresqlDatabase(
    os.getenv('PGDATABASE', 'delivery_management_system'),
    user=os.getenv('PGUSER', 'postgres'),
    password=os.getenv('PGPASSWORD', 'postgres'),
    host=os.getenv('PGHOST', 'localhost'),
    port=int(os.getenv('PGPORT', 5432)),
    max_connections=20,
    stale_timeout=300  # Close connections not used for 5 minutes
)
