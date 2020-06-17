<template>
  <div>
    <div v-show="$auth.loggedIn">
      <!-- NAVBAR WHEN AUTHENTICATED -->
      <NavbarTaxAuth class="pr-5" />
    </div>
    <div v-show="!$auth.loggedIn">
      <!-- NAVBAR WHEN NOT AUTHENTICATED -->
      <NavbarUnauth class="pr-5" />
    </div>
  </div>
</template>

<script>
import NavbarTaxAuth from './NavbarTaxAuth'
import NavbarUnauth from '../NavbarUnauth'

export default {
  name: 'NavbarTax',
  components: {
    NavbarTaxAuth,
    NavbarUnauth,
  }
}
</script>
