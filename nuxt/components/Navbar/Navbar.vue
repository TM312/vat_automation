<template>
  <div>
    <div v-show="$auth.loggedIn">
      <!-- NAVBAR WHEN AUTHENTICATED -->
      <NavbarAuth class="pr-5" />
    </div>
    <div v-show="!$auth.loggedIn">
      <!-- NAVBAR WHEN NOT AUTHENTICATED -->
      <NavbarUnauth class="pr-5" />
    </div>
  </div>
</template>

<script>
import NavbarAuth from './NavbarAuth'
import NavbarUnauth from './NavbarUnauth'

export default {
  middleware: 'auth',
  name: 'Navbar',
  components: {
    NavbarAuth,
    NavbarUnauth,
  },
  // data() {
  //   return {
  //     show_nav: true
  //   }
  // },
  // created() {
  //   if (this.$route.path == '/login') {
  //     this.show_nav = false
  //   } else {
  //     this.show_nav = true
  //   }
  // }
}
</script>
