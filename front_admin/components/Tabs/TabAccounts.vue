<template>
  <div>
    <h1 class="mb-5">
      Here gets all Account Data
    </h1>
    <table-accounts />
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "TabAccounts",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.accounts.length === 0) {
      await store.dispatch("accounts/get_all")
    }
  },
  computed: {
    ...mapState({
      accounts: (state) => state.account.accounts,
    }),
  },
}
</script>

<style>
</style>
