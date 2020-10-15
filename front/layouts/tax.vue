<template>
  <div>
    <navbar-tax />
    <div class="app-body">
      <!-- <h1>THIS IS THE TAX LAYOUT</h1> -->
      <nuxt />
    </div>
    <Footer />
  </div>
</template>

<script>
    export default {
        middleware: 'auth',

        mounted() {
            this.socket = this.$nuxtSocket({
                name: 'home',
                reconnection: true
            })
        }
    }
</script>
