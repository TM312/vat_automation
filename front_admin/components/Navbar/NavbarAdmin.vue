<template>
  <div>
    <b-navbar toggleable="lg" type="light" variant="light">
      <b-navbar-brand to="/">
        Tax-Automation
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" />

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/dashboard">
            Dashboard
          </b-nav-item>
          <b-nav-item to="/seller-firms">
            Seller Firms
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <navbar-auth-avatar-dropdown />
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "NavbarAdmin",
  mounted() {
    this.socket = this.$nuxtSocket({
      name: "home",
      reconnection: true,
    })
  },
}
</script>
