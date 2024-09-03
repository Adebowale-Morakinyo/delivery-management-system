# Delivery Management System

This project is a Delivery Management System (DMS) that allocates delivery orders to agents while optimizing for efficiency and meeting certain compliances.

## Technologies Used

- Backend: Python with Falcon framework
- Frontend: Vue.js
- Database: PostgreSQL
- Deployment: Docker and Docker Compose

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your system
- Git

### Local Development

1. Clone the repository:
   
   git clone https://github.com/Adebowale-Morakinyo/delivery-management-system.git
   
   cd delivery-management-system
   

2. Create a `.env` file in the root directory with the following content:
   
   DATABASE_URL=postgresql://user:password@db:5432/delivery_management_system
   

3. Build and run the Docker containers:
   
   docker-compose up --build
   

4. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000

## API Documentation

### Warehouses

- GET /warehouses: Retrieve all warehouses
- POST /warehouses: Create a new warehouse

### Agents

- GET /agents: Retrieve all agents
- POST /agents: Create a new agent
- POST /agents/{agent_id}/check-in: Check-in an agent

### Orders

- GET /orders: Retrieve all orders
- POST /orders: Create a new order

## Frontend Usage Guide

The frontend displays a simple dashboard showing key metrics:
- Total Orders
- Allocated Orders
- Pending Orders
- Active Agents
- Average Orders per Agent (derived metric)

## Deployment

To deploy the application:

1. Ensure you have Docker and Docker Compose installed on your server.
2. Clone the repository on your server.
3. Create a `.env` file with the appropriate database credentials.
4. Run `docker-compose up -d` to start the application in detached mode.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
