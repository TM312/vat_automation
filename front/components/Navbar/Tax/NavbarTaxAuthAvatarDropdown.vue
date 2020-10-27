<template>
  <b-nav-item-dropdown right no-caret>
    <template slot="button-content">
      <b-avatar variant="primary" :text="initials" />
    </template>
    <b-dropdown-header tag="div" class="text-center" variant="primary">
      <strong>Account</strong>
    </b-dropdown-header>

    <b-dropdown-item to="/tax/settings">
      <b-icon icon="gear" /> Settings
    </b-dropdown-item>
    <!-- <b-dropdown-item to="/payments">
            <b-icon icon="credit-card" />
            Invoices
            <b-badge v-if="payments" variant="primary">new</b-badge>
        </b-dropdown-item> -->
    <b-dropdown-divider />
    <b-dropdown-item @click="logout">
      <b-icon icon="power" /> Logout
    </b-dropdown-item>
  </b-nav-item-dropdown>
</template>

<script>
import { BIcon } from "bootstrap-vue"
export default {
  name: "NavbarTaxAuthAvatarDropdown",
  components: {
    BIcon
  },
  data() {
    return {
      payments: true
    }
  },
  computed: {
    initials() {
      return this.$auth.user.initials
    }
  },
  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push("/logout")
    }
  },
}
</script>

<style></style>
