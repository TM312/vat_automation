<template>
  <div>
    <b-row align-h="start">
      <b-col cols="auto">
        <container-route-back />
      </b-col>
      <b-col v-if="$fetchState.pending && (taxRecord.public_id != $route.params.public_id || taxRecord.length == 0)" />
      <b-col v-else>
        <h3 class="text-muted text-center">
          {{ sellerFirm.name }}
        </h3>
      </b-col>
    </b-row>
    <hr />

    <b-container fluid>
      <b-tabs pills card vertical>
        <b-tab title="Overview" active>
          <card-tax-record-loading v-if="$fetchState.pending && (taxRecord.public_id != $route.params.public_id || taxRecord.length == 0)" />
          <card-tax-record v-else />
          <container-tax-record-tables />
        </b-tab>

        <b-tab title="Transactions" lazy>
          <b-card v-if="$fetchState.pending && (taxRecord.public_id != $route.params.public_id || taxRecord.length == 0)" lazy />
          <overview-transactions />
        </b-tab>
      </b-tabs>
    </b-container>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  layout: 'tax',

  async fetch() {
    const { store } = this.$nuxt.context
    await store.dispatch('tax_record/get_by_public_id', this.$route.params.public_id)
    if (this.sellerFirm.length == 0 || this.taxRecord.seller_firm_public_id !== this.sellerFirm.public_id) {
      await store.dispatch('seller_firm/get_by_public_id', this.taxRecord.seller_firm_public_id)
    }

  },

  computed: {
    ...mapState({
      taxRecord: state => state.tax_record.tax_record,
      sellerFirm: state => state.seller_firm.seller_firm
    }),
  }

}
</script>

<style></style>
