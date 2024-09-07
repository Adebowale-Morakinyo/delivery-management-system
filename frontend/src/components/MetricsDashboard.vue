<template>
  <div class="metrics-dashboard">
    <h2>Metrics Dashboard</h2>

    <!-- Show loading state while data is being fetched -->
    <div v-if="loading" class="loading-message">
      <font-awesome-icon :icon="['fas', 'spinner']" spin class="loading-icon" />
      <p>Loading metrics...</p>
    </div>

    <!-- Show error message if there was an error fetching data -->
    <div v-if="error" class="error-message">
      <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
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
        allocatedOrders: ['fas', 'check-circle'],
        pendingOrders: ['fas', 'clock'],
        activeAgents: ['fas', 'user-check']
      };
      return icons[key] || ['fas', 'info-circle']; // Default icon
    }
  }
}
</script>
