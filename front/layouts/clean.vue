<template>
  <div>
    <div class="app-body">
      <!-- <h1>THIS IS THE DEFAULT LAYOUT</h1> -->
      <nuxt />
    </div>
    <Footer />
  </div>
</template>


<script>
import Footer from '@/components/Footer'

export default {
  components: {
    Footer
  },
}
</script>
