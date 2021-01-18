<template>
  <b-sidebar
    id="sidebar-transaction"
    title="Transaction Details"
    right
    shadow
    width="500px"
  >
    <div class="px-3 py-2">
      <p>
        Here you find a summary of the tax related key figures. By clicking on the button below you are being directed to the original transaction that provides more details.
      </p>
      <b-button size="sm" variant="outline-primary" class="mt-3" :to="`/transactions/${transaction.transaction_input_public_id}`" exact>
        <b-icon icon="arrow-right" /> Go to Transaction
      </b-button>
    </div>
    <div v-if="transactionPublicId !== ''" class="mt-3">
      <card-transaction-base-data :transaction="transaction" />
      <card-transaction-prices :transaction="transaction" class="mt-3" />
    </div>
  </b-sidebar>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "SidebarTransaction",
  props: {
    transactionPublicId: {
      type: String,
      required: true,
    },
  },

  computed: {
    ...mapState({
      sellerFirmPublicId: state => state.seller_firm.seller_firm.public_id
    }),
    transaction() {
      return this.$store.getters["transaction/getByPublicId"](this.transactionPublicId)
    }

  },
}
</script>

<style>
</style>
