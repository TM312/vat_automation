<template>
  <div>
    <div v-show="$auth.loggedIn">
      <!-- NAVBAR WHEN AUTHENTICATED -->
      <navbar-tax-auth class="pr-5" />
    </div>
    <div v-show="!$auth.loggedIn">
      <!-- NAVBAR WHEN NOT AUTHENTICATED -->
      <navbar-unauth class="pr-5" />
    </div>
  </div>
</template>

<script>
export default {
  name: "NavbarTax",
  mounted() {
    this.socket = this.$nuxtSocket({
      name: "home",
      reconnection: true,
    })
  },
}
</script>
