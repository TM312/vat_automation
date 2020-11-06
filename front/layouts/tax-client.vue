<template>
  <div>
    <navbar-tax />
    <b-container fluid>
      <h3 class="text-muted text-center my-3">
        {{ sellerFirm.name }}
      </h3>
      <b-row class="my-3">
        <b-col cols="auto">
          <navbar-tax-side :client-public-id="sellerFirm.public_id" />
        </b-col>
        <b-col>
          <nuxt />
        </b-col>
      </b-row>
      <!-- <h1>THIS IS THE TAX LAYOUT</h1> -->
    </b-container>
    <Footer />

    <!-- Toasts for various purposes -->
    <toasts-static-data-upload />
    <toast-new-tax-record />
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  middleware: "auth",

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
    }),
  },

  beforeDestroy() {
    this.resetStoreSellerFirm()
  },

  methods: {
    resetStoreSellerFirm() {
      const { store } = this.$nuxt.context
      store.dispatch("seller_firm/clear_seller_firm")

      // clear complete states
      store.dispatch("status/clear_all")
      store.dispatch("transaction_input/clear_state")
      store.dispatch("tax_record/clear_state")
      store.dispatch("transaction/clear_state")
    },
  },
}
</script>
