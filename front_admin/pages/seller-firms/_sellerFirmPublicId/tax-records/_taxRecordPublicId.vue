<template>
  <div class="mt-3">
    <b-row>
      <b-col v-if="detailsOn" cols="auto">
        <b-button variant="outline-info" @click="toggleView">
          <!-- #//:to="`/seller-firms/${clientPublicId}/tax-records`" exact -->
          <b-icon icon="arrow-left" /> Back
        </b-button>
      </b-col>
      <b-col>
        <card-tax-record-loading
          v-if="
            $fetchState.pending &&
              (taxRecord.public_id != taxRecordPublicId ||
                taxRecord.length == 0)
          "
        />
        <card-tax-record v-else />
      </b-col>
    </b-row>
    <b-tabs class="mt-3">
      <b-tab title="Summary" active>
        <container-tax-record-tables class="mt-3" />
      </b-tab>

      <b-tab title="Transactions" lazy :disabled="$fetchState.pending">
        <overview-transactions
          class="mt-3"
          @getDetails="toggleView"
          @new-tab="newTab;"
        />
      </b-tab>

      <!-- <b-tab v-for="(transactionInput, i) in transactionInputs" :key="i" :title="transactionInput.">
        <container-transaction-input :client-public-id="clientPublicId" :transaction-input-public-id="transactionInput.public_id" /> -->
      <!-- <b-button size="sm" variant="danger" class="float-right" @click="closeTab(i)"  >
          Close tab
        </b-button> -->
      <!-- </b-tab> -->
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: "admin-seller-firm",

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
  async asyncData({ params }) {
    const clientPublicId = params.clientPublicId
    const taxRecordPublicId = params.taxRecordPublicId
    return { taxRecordPublicId, clientPublicId }
  },
  data() {
    return {
      detailsOn: false,
      tabs: [],
      tabCounter: 0,
    }
  },

  computed: {
    ...mapState({
      taxRecord: (state) => state.tax_record.tax_record,
      sellerFirm: (state) => state.seller_firm.seller_firm,
    }),
  },
  methods: {
    toggleView() {
      this.detailsOn = !this.detailsOn
    },
    closeTab(x) {
      for (let i = 0; i < this.tabs.length; i++) {
        if (this.tabs[i] === x) {
          this.tabs.splice(i, 1)
        }
      }
    },
    newTab() {
      this.tabs.push(this.tabCounter++)
    },
  },
}
</script>

<style>
</style>
