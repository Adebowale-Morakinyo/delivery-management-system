<template>
  <div class="metrics-dashboard">
    <h2>Metrics Dashboard</h2>

    <!-- Show loading state while data is being fetched -->
    <div v-if="loading" class="loading-message">
      <font-awesome-icon :icon="['fas', 'spinner']" spin />
      <p>Loading metrics...</p>
    </div>

    <!-- Show error message if there was an error fetching data -->
    <div v-if="error" class="error-message">
      <font-awesome-icon :icon="['fas', 'triangle-exclamation']" />
      <p>Error loading metrics. Please try again later.</p>
    </div>

    <!-- Show metrics after data has been loaded -->
    <div v-else-if="!loading" class="metrics">
      <div class="metric" v-for="(value, key) in metrics" :key="key">
        <font-awesome-icon :icon="getIcon(key)" class="metric-icon" />
        <h3>{{ formatMetricTitle(key) }}</h3>
        <p>{{ value }}</p>
      </div>
      <div class="metric">
        <font-awesome-icon :icon="['fas', 'users']" />
        <h3>Average Orders per Agent</h3>
        <p>{{ averageOrdersPerAgent }}</p>
      </div>
    </div>
  </div>
</template>

<script>
// import { faSpinner, faExclamationTriangle, faBox, faCheckCircle, faClock, faUserCheck, faUsers, faInfoCircle } from '@fortawesome/free-solid-svg-icons';
import api from '../api/config'

export default {
  name: 'MetricsDashboard',
  data() {
    return {
      metrics: {},    // Will be populated with metrics data
      loading: true,  // Loading state for API call
      error: false,   // Error state for API call
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
    this.fetchMetrics()  // Fetch the metrics when component is mounted
  },
  methods: {
    async fetchMetrics() {
      try {
        const response = await api.get('/metrics')  // Fetch all metrics from new endpoint
        this.metrics = response.data  // Set metrics data from API response
      } catch (error) {
        console.error('Error fetching metrics:', error)
        this.error = true  // Set error state if there is an issue
      } finally {
        this.loading = false  // Ensure loading is false after fetching is done
      }
    },
    formatMetricTitle(key) {
      // Format the key string into a more human-readable title
      return key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1')
    },
    getIcon(key) {
      const icons = {
        totalOrders: ['fas', 'box'],
        allocatedOrders: ['fas', 'circle-check'],
        pendingOrders: ['fas', 'clock'],
        activeAgents: ['fas', 'user-check']
      };
      return icons[key] || ['fas', 'circle-info']; // Default icon
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