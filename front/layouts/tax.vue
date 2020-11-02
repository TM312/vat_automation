<template>
  <div>
    <navbar-tax />
    <div class="app-body">
      <b-row cols="2">
        <b-col cols="auto">
          <navbar-tax-side />
        </b-col>
        <b-col>
          <nuxt />
        </b-col>
      </b-row>
      <!-- <h1>THIS IS THE TAX LAYOUT</h1> -->
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
