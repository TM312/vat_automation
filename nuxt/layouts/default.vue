<template>
  <div>
    <Navbar />
    <div class="app-body">
      <nuxt />
    </div>
    <Footer />
  </div>
</template>

<script>
import { Navbar, Footer } from '@/components/'
export default {
  components: {
    Navbar,
    Footer,
  },
}
</script>
