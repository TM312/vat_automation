<template>
  <b-navbar toggleable="lg" type="light" variant="light">
    <b-navbar-brand to="/">
      AMZ
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse" />

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/dashboard">
          Dashboard
        </b-nav-item>
      </b-navbar-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <NavbarAuthDropdown />
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import NavbarAuthDropdown from './NavbarAuthDropdown'

// import { BIcon } from 'bootstrap-vue'
export default {
  middleware: 'auth',
  name: 'NavbarAuth',
  components: {
    NavbarAuthDropdown
    // BIcon
  }
}
</script>

<style></style>
