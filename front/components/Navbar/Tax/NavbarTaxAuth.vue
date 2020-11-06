<template>
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
        <!-- ^integrate v-if for multiple user roles -->
        <b-nav-item to="/clients">
          Clients
        </b-nav-item>
        <!-- <b-nav-item to="/tax_records" :disabled="accounting_firm.length === 0">Tax Records</b-nav-item> -->
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <navbar-tax-auth-avatar-dropdown />
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
// import { mapState } from 'vuex'
export default {
  name: "NavbarTaxAuth",
  // computed: {
  //     ...mapState({
  //         accounting_firm: state => state.accounting_firm.accounting_firm
  //     })

  // }
}

</script>
