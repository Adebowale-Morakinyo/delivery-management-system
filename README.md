# Delivery Management System

## Overview

This Delivery Management System is a web application designed to allocate delivery orders to agents while optimizing for efficiency and meeting certain compliances. The system consists of a Python backend using the Falcon framework and a Vue.js frontend.

## Features

- Dashboard displaying key metrics
- Agent check-in functionality
- Order allocation view
- Automatic order allocation based on efficiency and compliance rules

## Tech Stack

- Backend: Python with Falcon framework
- Frontend: Vue.js
- Database: PostgreSQL
- ORM: Peewee
- State Management: Vuex
- Testing: Python unittest, Jest, Vue Test Utils
- Containerization: Docker

## Project Structure

```
delivery-management-system/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── store/
│   │   ├── App.vue
│   │   └── main.js
│   ├── tests/
│   └── package.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/delivery-management-system.git
   cd delivery-management-system
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

4. Set up the database:
   - Install PostgreSQL
   - Create a new database named `delivery_management_system`

5. Update the database connection settings in `backend/app/database.py`

## Running the Application

1. Start the backend server:
   ```
   cd backend
   python app/main.py
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm run serve
   ```

3. Access the application at `http://localhost:8080`

## Running Tests

1. Backend tests:
   ```
   cd backend
   python -m unittest discover tests
   ```

2. Frontend tests:
   ```
   cd frontend
   npm run test
   ```

## Deployment

The application can be deployed using Docker. Make sure you have Docker and Docker Compose installed on your system.

1. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000`

## API Documentation

### Warehouses

- GET /warehouses: Retrieve all warehouses
- POST /warehouses: Create a new warehouse

### Agents

- GET /agents: Retrieve all agents
- POST /agents: Create a new agent

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

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
