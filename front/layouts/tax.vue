<template>
  <div>
    <navbar-tax />
    <b-container fluid>
      <nuxt />
    </b-container>
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
