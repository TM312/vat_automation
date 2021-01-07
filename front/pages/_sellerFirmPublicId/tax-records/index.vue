<template>
  <div>
    <b-tabs content-class="mt-3">
      <b-tab title="Overview" active>
        <div v-if="$fetchState.pending">
          <view-tax-records-skeleton />
        </div>
        <div v-else>
          <view-tax-records :seller-firm="sellerFirm" :tax-records="taxRecords" />
        </div>
      </b-tab>
      <b-tab title="Create New">
        <lazy-form-add-seller-firm-tax-record />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: 'tax-client',

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.taxRecords.length == 0) {
      await store.dispatch(
        "tax_record/get_all_by_seller_firm_public_id",
        this.sellerFirm.public_id
      )
    }
  },

  data() {
    return {
      taxRecordPublicId: "",
    }
  },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
      taxRecords: (state) => state.tax_record.tax_records
    }),
  },
}
</script>

<style>
</style>
