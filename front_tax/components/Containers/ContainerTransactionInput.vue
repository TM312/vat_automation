<template>
  <div v-if="clientPublicId.length > 0 && transactionInputPublicId.length > 0">
    <card-transaction-input-bundle :transaction-input-public-id="transactionInputPublicId" :client-public-id="clientPublicId" />
    <b-alert :show="!transactionInput.processed && !$fetchState.pending" variant="danger">
      <p>The transaction has not been processed yet due to network errors. Click here to retry: <button-validate-transaction-input :transaction-input-public-id="transactionInputPublicId" /> </p>
    </b-alert>
    <b-tabs class="mt-3">
      <b-tab title="Input File" active>
        <div v-if="$fetchState.pending || transactionInput.length === 0"></div>
        <card-transaction-input v-else id="file" />
      </b-tab>

      <b-tab title="Tax Processes" lazy :disabled="$fetchState.pending && sellerFirm.public_id != clientPublicId || transactionInput.length === 0">
        <span v-if="$fetchState.pending || transactionInput.length === 0"></span>
        <view-transactions v-else :transactions="transactionInput.transactions" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ContainerTransactionInput',
  props: {
    clientPublicId: {
      type: String,
      required: false,
      default: ''
    },
    transactionInputPublicId: {
      type: String,
      required: false,
      default: ''
    }
  },

  async fetch() {
    if (this.transactionInputPublicId && this.transactionInput.public_id !== this.transactionInputPublicId) {
      const { store } = this.$nuxt.context
      await store.dispatch('transaction_input/get_by_public_id', this.transactionInputPublicId)
    }
  },


  computed: {
    ...mapState({
      transactionInput: state => state.transaction_input.transaction_input,
      transactionInputsBundle: state => state.transaction_input.transaction_inputs_bundle,
      sellerFirm: state => state.seller_firm.seller_firm
    }),
  }


}
</script>

<style></style>
