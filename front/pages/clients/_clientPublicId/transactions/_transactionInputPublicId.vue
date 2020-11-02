<template>
  <div fluid>
    <b-alert :show="!transactionInput.processed && !$fetchState.pending" variant="danger">
      <p>The transaction has not been processed yet due to network errors. Click here to retry: <button-validate-transaction-input :transaction-input-public-id="transactionInputPublicId" /> </p>
    </b-alert>
    <b-tabs pills card>
      <b-tab title="Input File" active>
        <div v-if="$fetchState.pending || transactionInput.length === 0"></div>
        <card-transaction-input v-else id="file" />

        <b-card title="Transaction Bundle" sub-title="A list of all related transactions" class="mt-4">
          <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
          <table-transaction-inputs v-else :transaction-inputs="transactionInputsBundle" class="mt-4" />
        </b-card>
      </b-tab>

      <b-tab title="Tax Processes" lazy :disabled="$fetchState.pending && sellerFirm.public_id != clientPublicId || transactionInput.length === 0">
        <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
        <view-transactions v-else :transactions="transactionInput.transactions" />

        <b-card title="Transaction Bundle" sub-title="A list of all related transactions" class="mt-4">
          <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
          <table-transaction-inputs v-else :transaction-inputs="transactionInputsBundle" />
        </b-card>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: 'tax-client',

  async fetch() {
    if (this.transactionInput.public_id !== this.transactionInputPublicId) {
      const { store } = this.$nuxt.context
      await store.dispatch('transaction_input/get_by_public_id', this.transactionInputPublicId)
    }
  },

  async asyncData({ params }) {
    const clientPublicId = params.clientPublicId
    const transactionInputPublicId = params.transactionInputPublicId
    return { transactionInputPublicId, clientPublicId }
  },


  computed: {
    ...mapState({
      transactionInput: state => state.transaction_input.transaction_input,
      transactionInputsBundle: state => state.transaction_input.transaction_inputs_bundle,
      sellerFirm: state => state.seller_firm.seller_firm
    }),
  },

  // beforeDestroy() {
  //     this.clearStoreTransactionInputs()
  // },

  // methods: {
  //     clearStoreTransactionInputs() {
  //         const { store } = this.$nuxt.context
  //         store.dispatch('transaction_input/clear_transaction_inputs_bundle')
  //     }

  // },

}
</script>
