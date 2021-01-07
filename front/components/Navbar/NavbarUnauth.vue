<template>
  <b-navbar toggleable="lg" type="light" variant="white" style="opacity:0.8">
    <b-navbar-brand to="/">
      Tax-Automation
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse" />

    <b-collapse id="nav-collapse" is-nav>
      <!-- <b-navbar-nav>
        <b-nav-item to="/">
          <i>Navbar items...</i>
        </b-nav-item>
      </b-navbar-nav> -->

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item to="/pricing" :active="currentRouteName == 'pricing'">
          Pricing
        </b-nav-item>
        <b-nav-item to="/register" :active="currentRouteName == 'register' ">
          Sign Up
        </b-nav-item>
        <!-- Using 'button-content' slot -->
        <!-- <b-button variant="outline-success" to="/login">
          Sign In
        </b-button> -->
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'NavbarUnauth',
  computed: {
    currentRouteName() {
      return this.$route.name
    }
  }

}
</script>

<style></style>
