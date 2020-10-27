<template>
  <b-container fluid>
    <b-tabs pills card vertical>
      <b-tab title="Overview" active @click="refresh">
        <clients-dashboard />
        <view-clients class="mt-5" />
      </b-tab>
      <b-tab title="Add Clients" lazy>
        <lazy-container-add-client />
      </b-tab>
    </b-tabs>
  </b-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: 'tax',

  computed: {
    ...mapState({
      accountingFirm: state => state.accounting_firm.accounting_firm
    }),

    countClients() {
      return this.$store.getters['accounting_firm/countClients']
    },
  },

  methods: {
    async refresh() {
      const { store } = this.$nuxt.context
      await store.dispatch("accounting_firm/get_by_public_id", this.accountingFirm.public_id)
    }
  },
}
</script>

<style></style>
