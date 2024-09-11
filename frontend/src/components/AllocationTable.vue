vue
<template>
  <div class="allocation-table">
    <h2>Order Allocation Details</h2>

    <!-- Show loading state while data is being fetched -->
    <div v-if="loading" class="loading-message">
      <font-awesome-icon :icon="['fas', 'spinner']" spin class="loading-icon themed-icon" />
      <p>Loading allocation details...</p>
    </div>

    <!-- Show error message if there was an error fetching data -->
    <div v-if="error" class="error-message">
      <font-awesome-icon :icon="['fas', 'triangle-exclamation']" class="error-icon themed-icon" />
      <p>Error loading allocation details. Please try again later.</p>
    </div>

    <!-- Show table after data has been loaded -->
    <div v-else-if="!loading" class="table-container">
      <table>
        <thead>
          <tr>
            <th>Agent Name</th>
            <th>Order ID</th>
            <th>Estimated Distance (km)</th>
            <th>Estimated Time (hours)</th>
            <th>Allocation Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="allocation in allocations" :key="allocation.orderId">
            <td>{{ allocation.agentName }}</td>
            <td>{{ allocation.orderId }}</td>
            <td>{{ allocation.estimatedDistance ? allocation.estimatedDistance.toFixed(2) : 'N/A' }}</td>
            <td>{{ allocation.estimatedTime ? allocation.estimatedTime.toFixed(2) : 'N/A' }}</td>
            <td>{{ allocation.allocationTimestamp }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../api/config'

export default {
  name: 'AllocationTable',
  data() {
    return {
      allocations: [],
      loading: true,
      error: false,
    }
  },
  mounted() {
    this.fetchAllocationDetails()
  },
  methods: {
    async fetchAllocationDetails() {
      try {
        const response = await api.get('/allocation-details')
        this.allocations = response.data
      } catch (error) {
        console.error('Error fetching allocation details:', error)
        this.error = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.allocation-table {
  max-width: 900px; /* Match the max-width of MetricsDashboard */
  margin: 20px auto; /* Center the component with margin */
  padding: 20px; /* Add padding for better spacing */
  background: linear-gradient(135deg, #f7f8f9, #e1e4e8); /* Add a background similar to MetricsDashboard */
  border-radius: 10px; /* Match border radius */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Add shadow for depth */
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

thead th {
  background-color: #007bff;
  color: white;
  padding: 10px;
}

tbody td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.loading-message,
.error-message {
  text-align: center;
  font-size: 1.5em;
  color: #333;
}
</style>