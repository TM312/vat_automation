<template>
  <container-transaction-input :client-public-id="clientPublicId" :transaction-input-public-id="transactionInputPublicId" />
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: 'admin-seller-firm',

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

}
</script>
