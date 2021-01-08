<template>
  <container-transaction-input :client-public-id="sellerFirmPublicId" :transaction-input-public-id="transactionInputPublicId" />
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: 'tax-client',

  async asyncData({ params }) {
    const sellerFirmPublicId = params.sellerFirmPublicId
    const transactionInputPublicId = params.transactionInputPublicId
    return { transactionInputPublicId, sellerFirmPublicId }
  },


  computed: {
    ...mapState({
      transactionInput: state => state.transaction_input.transaction_input,
      transactionInputsBundle: state => state.transaction_input.transaction_inputs_bundle,
      sellerFirm: state => state.seller_firm.seller_firm
    }),
  },

}
</script>
