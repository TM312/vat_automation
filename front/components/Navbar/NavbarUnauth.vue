<template>
  <b-navbar toggleable="lg" type="light" variant="light">
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
        <!-- Using 'button-content' slot -->
        <b-button variant="outline-success" to="/tax/login">
          Sign In
        </b-button>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'NavbarUnauth',
}
</script>

<style></style>
