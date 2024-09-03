# delivery-management-system








## **Local PostgreSQL Database Setup**

### **1. Database Schema Creation**
For the development and testing phase, I set up a PostgreSQL database locally. This was done to ensure smooth development and testing without relying on external hosting services, which may have downtime. The following schema was used to create the necessary tables:

```sql
-- Create the warehouses table
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL
);

-- Create the agents table
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    warehouse_id INTEGER REFERENCES warehouses(id),
    check_in_time TIMESTAMP,
    total_orders INTEGER DEFAULT 0,
    total_distance DECIMAL(10, 2) DEFAULT 0,
    total_time DECIMAL(10, 2) DEFAULT 0
);

-- Create the orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    warehouse_id INTEGER REFERENCES warehouses(id),
    delivery_address VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    agent_id INTEGER REFERENCES agents(id),
    allocated_date DATE,
    completed_time TIMESTAMP
);
```

### **2. Local PostgreSQL Database Connection Using Peewee**

For connecting the local PostgreSQL database to the backend, I used Peewee, a small and expressive ORM. The connection details are specified in the `backend/app/database.py` file, which ensures that the application interacts with the database seamlessly during development and testing.

### **3. Reason for Local Development and Testing**

The choice to use a local PostgreSQL instance, alongside Peewee for ORM, was made for the following reasons:

- **Development & Testing:** By hosting the database locally, I can ensure that development and testing processes are not disrupted by potential downtime of third-party hosting services.
- **Fallback Plan:** While the project will eventually be hosted, using a local database allows me to proceed with development without delays. In case the hosting service (e.g., Railway) is not available before the production deadline, this setup ensures that I have a fully functional application ready for deployment.
