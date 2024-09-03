<template>
  <div id="app">
    <h1>Delivery Management System</h1>
    <metrics-dashboard />
  </div>
</template>

<script>
import MetricsDashboard from './components/MetricsDashboard.vue'

export default {
  name: 'App',
  components: {
    MetricsDashboard
  }
}
</script>