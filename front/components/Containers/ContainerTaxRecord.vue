<template>
  <div class="mt-3">
    <b-row>
      <b-col cols="auto">
        <b-button variant="outline-info" @click="$emit('overview')">
          <b-icon icon="arrow-left" /> Go Back
        </b-button>
      </b-col>
      <b-col>
        <card-tax-record-loading v-if="$fetchState.pending && (taxRecord.public_id != taxRecordPublicId || taxRecord.length == 0)" />
        <card-tax-record v-else />
      </b-col>
    </b-row>
    <b-tabs class="mt-3">
      <b-tab title="Summary" active>
        <container-tax-record-tables class="mt-3" />
      </b-tab>

      <b-tab title="Transactions" lazy :disabled="$fetchState.pending">
        <overview-transactions class="mt-3" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "ContainerTaxRecord",

  props: {
    taxRecordPublicId: {
      type: String,
      required: true,
    },
  },

  async fetch() {
    const { store } = this.$nuxt.context
    await store.dispatch(
      "tax_record/get_by_public_id",
      this.taxRecordPublicId
    )
    if (
      this.sellerFirm.length == 0 ||
                this.taxRecord.seller_firm_public_id !== this.sellerFirm.public_id
    ) {
      await store.dispatch(
        "seller_firm/get_by_public_id",
        this.taxRecord.seller_firm_public_id
      )
    }
  },

  computed: {
    ...mapState({
      taxRecord: (state) => state.tax_record.tax_record,
      sellerFirm: (state) => state.seller_firm.seller_firm,
    }),
  },
}
</script>

<style></style>
