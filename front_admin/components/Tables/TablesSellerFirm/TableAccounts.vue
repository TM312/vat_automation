<template>
  <b-table :items="accounts" />
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'TableAccounts',

  computed: {
    ...mapState({
      accounts: state => state.account.accounts
    })
  },

}
</script>
