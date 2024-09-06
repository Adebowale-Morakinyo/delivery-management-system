<template>
    <div class="metrics-dashboard">
      <h2>Metrics Dashboard</h2>
  
      <!-- Show loading state while data is being fetched -->
      <div v-if="loading" class="loading-message">
        <p>Loading metrics...</p>
      </div>
  
      <!-- Show error message if there was an error fetching data -->
      <div v-if="error" class="error-message">
        <p>Error loading metrics. Please try again later.</p>
      </div>
  
      <!-- Show metrics after data has been loaded -->
      <div v-else-if="!loading" class="metrics">
        <div class="metric" v-for="(value, key) in metrics" :key="key">
          <h3>{{ formatMetricTitle(key) }}</h3>
          <p>{{ value }}</p>
        </div>
        <div class="metric">
          <h3>Average Orders per Agent</h3>
          <p>{{ averageOrdersPerAgent }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../api/config'
  
  export default {
    name: 'MetricsDashboard',
    data() {
      return {
        metrics: {
          totalOrders: 0,
          allocatedOrders: 0,
          pendingOrders: 0,
          activeAgents: 0
        },
        loading: true, // Add loading state
        error: false,  // Add error state
      }
    },
    computed: {
      averageOrdersPerAgent() {
        return this.metrics.activeAgents
          ? (this.metrics.allocatedOrders / this.metrics.activeAgents).toFixed(2)
          : '0.00'
      }
    },
    mounted() {
      this.fetchMetrics()
    },
    methods: {
      async fetchMetrics() {
        try {
          // Increase timeout to 120 seconds for API calls
          const [ordersResponse, agentsResponse] = await Promise.all([
            api.get('/orders'),
            api.get('/agents')
          ])
  
          // Log the API responses for debugging purposes
          console.log('Orders Response:', ordersResponse.data)
          console.log('Agents Response:', agentsResponse.data)
  
          // Extract and filter data from API responses
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
          this.error = true // Set error state if there is an issue
        } finally {
          this.loading = false // Ensure loading is false after fetching is done
        }
      },
      formatMetricTitle(key) {
        return key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1')
      }
    }
  }
  </script>
  
  <style scoped>
  .metrics-dashboard {
    max-width: 900px;
    margin: 20px auto;
    padding: 20px;
    background: linear-gradient(135deg, #f7f8f9, #e1e4e8);
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
  
  .metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .metric {
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;
    text-align: center;
  }
  
  .metric:hover {
    transform: translateY(-5px);
  }
  
  .metric h3 {
    margin-top: 0;
    color: #333;
    font-size: 1.2em;
  }
  
  .metric p {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 0;
    color: #007bff;
  }
  
  .loading-message,
  .error-message {
    text-align: center;
    font-size: 1.5em;
    color: #333;
  }
  
  .error-message {
    color: red;
  }
  </style>
  