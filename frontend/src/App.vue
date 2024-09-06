vue
<template>
  <div id="app">
    <h1 class="app-heading">Delivery Management System</h1>
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

<style scoped>
.app-heading {
  text-align: center; /* Center the heading */
  font-size: 2.5em; /* Set font size */
  font-weight: bold; /* Make the font bold */
  color: #333; /* Dark gray color for the text */
  margin: 20px 0; /* Add margin above and below the heading */
  text-transform: uppercase; /* Transform text to uppercase */
  letter-spacing: 2px; /* Add spacing between letters */
  background: linear-gradient(90deg, #007bff, #00c6ff); /* Gradient Background */
  -webkit-background-clip: text; /* Clip background to text */
  -webkit-text-fill-color: transparent; /* Make text color transparent to show gradient */
  animation: fadeIn 1s ease; /* Fade-in animation */
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
