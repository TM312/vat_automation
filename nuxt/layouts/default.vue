<template>
  <div>
    <NavbarUnauth />
    <div class="app-body">
      <!-- <h1>THIS IS THE DEFAULT LAYOUT</h1> -->
      <nuxt />
    </div>
    <Footer />
  </div>
</template>

<script>
import NavbarUnauth from '@/components/Navbar/NavbarUnauth'
import Footer from '@/components/Footer'

export default {
  components: {
    NavbarUnauth,
    Footer,
  },
}
</script>
