<template>
    <div class="metrics-dashboard">
      <h2>Metrics Dashboard</h2>
      <div class="metrics">
        <div class="metric">
          <h3>Total Orders</h3>
          <p>{{ metrics.totalOrders }}</p>
        </div>
        <div class="metric">
          <h3>Allocated Orders</h3>
          <p>{{ metrics.allocatedOrders }}</p>
        </div>
        <div class="metric">
          <h3>Pending Orders</h3>
          <p>{{ metrics.pendingOrders }}</p>
        </div>
        <div class="metric">
          <h3>Active Agents</h3>
          <p>{{ metrics.activeAgents }}</p>
        </div>
        <div class="metric">
          <h3>Average Orders per Agent</h3>
          <p>{{ averageOrdersPerAgent }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'MetricsDashboard',
    data() {
      return {
        metrics: {
          totalOrders: 0,
          allocatedOrders: 0,
          pendingOrders: 0,
          activeAgents: 0
        }
      }
    },
    computed: {
      averageOrdersPerAgent() {
        return this.metrics.activeAgents ? 
          (this.metrics.allocatedOrders / this.metrics.activeAgents).toFixed(2) : 
          '0.00'
      }
    },
    mounted() {
      this.fetchMetrics()
    },
    methods: {
      async fetchMetrics() {
        try {
          const [ordersResponse, agentsResponse] = await Promise.all([
            axios.get('/api/orders'),
            axios.get('/api/agents')
          ])
  
          const orders = ordersResponse.data
          const agents = agentsResponse.data
  
          this.metrics = {
            totalOrders: orders.length,
            allocatedOrders: orders.filter(o => o.status === 'allocated').length,
            pendingOrders: orders.filter(o => o.status === 'pending').length,
            activeAgents: agents.filter(a => a.check_in_time).length
          }
        } catch (error) {
          console.error('Error fetching metrics:', error)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .metrics-dashboard {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .metrics {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .metric {
    flex-basis: calc(33.333% - 20px);
    margin: 10px;
    padding: 20px;
    background-color: #f0f0f0;
    border-radius: 5px;
    text-align: center;
  }
  
  .metric h3 {
    margin-top: 0;
  }
  
  .metric p {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 0;
  }
  </style>
  