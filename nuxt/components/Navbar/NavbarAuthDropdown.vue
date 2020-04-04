<template>
  <b-nav-item-dropdown right no-caret>
    <template slot="button-content">
      <b-img
        src="@/assets/img/avatars/6.jpg"
        rounded="circle"
        alt="Profile Image"
        height="40px"
      />
    </template>
    <b-dropdown-header tag="div" class="text-center" variant="primary">
      <strong>Account</strong>
    </b-dropdown-header>
    <!-- <b-dropdown-item to="/profile">
      <b-icon icon="person-fill" />
      Profile
    </b-dropdown-item> -->
    <b-dropdown-item to="/settings">
      <b-icon icon="gear" />
      Settings
    </b-dropdown-item>
    <b-dropdown-item to="/payments">
      <b-icon icon="credit-card" />
      Invoices
      <b-badge v-if="payments" variant="primary">
        new
      </b-badge>
    </b-dropdown-item>
    <b-dropdown-divider />
    <b-dropdown-item @click="logout">
      <b-icon icon="power" /> Logout
    </b-dropdown-item>
  </b-nav-item-dropdown>
</template>

<script>
import { BIcon } from 'bootstrap-vue'
export default {
  name: 'NavbarAuthDropdown',
  middleware: 'auth',
  components: {
    BIcon,
  },
  data() {
    return {
      payments: true,
    }
  },
  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push('/logout')
    },
  },
}
</script>

<style></style>
