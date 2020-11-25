<template>
  <div>
    <b-container class="py-5 top mb-4">
      <section-vat-compliance-top />
    </b-container>

    <b-container class="py-2">
      <section-vat-compliance-demo-introduction />
      <section-vat-compliance-data-upload class="section-data-upload" />
      <section-vat-compliance-company-information v-if="Object.keys(sellerFirm).length !== 0" class="section-company-info" />
    </b-container>

    <b-container class="py-5 section-tax-record">
      <section-vat-compliance-tax-records />
    </b-container>


    <b-container fluid class="py-5">
      <section-vat-compliance-transaction-overview />
    </b-container>

    <b-container class="py-5" style="max-width: 40rem">
      <section-sign-up-sellers />
    </b-container>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  layout: "default",

  //   async fetch() {
  //     const { store } = this.$nuxt.context

  //     if (this.countries.length === 0) {
  //       await store.dispatch("country/get_all")
  //     }

  //     if (this.currencies.length === 0) {
  //       await store.dispatch("currency/get_all")
  //     }

  //     if (this.taxTreatments.length === 0) {
  //       await store.dispatch("tax_treatment/get_all")
  //     }

  //     if (this.taxRateTypes.length === 0) {
  //       await store.dispatch("tax_rate_type/get_all")
  //     }

  //     if (this.channels.length === 0) {
  //       await store.dispatch("channel/get_all")
  //     }

  //     if (this.vatThresholds.length === 0) {
  //       await store.dispatch("vat_threshold/get_all")
  //     }

  //     if (this.sellerFirm.length === 0) {
  //       await store.dispatch("seller_firm/get_sample")
  //     }
  //   },

  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm,
    //   channels: (state) => state.channel.channels,
    //   countries: (state) => state.country.countries,
    //   currencies: (state) => state.currency.currencies,
    //   taxTreatments: (state) => state.tax_treatment.tax_treatments,
    //   taxRateTypes: (state) => state.tax_rate_type.tax_rate_types,
    //   vatThresholds: (state) => state.vat_threshold.vat_thresholds,
      //   transactionInputs: (state) => state.transaction_input.transaction_inputs,
    }),
  },
}
</script>

<style scoped>
    mark.red {
        color: #ff0000;
        background: none;
    }

    .neumorphism {
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }

    .top{
        max-width: 50rem;
        min-height: 10rem;
    }

    .section-data-upload{
        min-height: 38rem;
    }

    .section-company-info{
        min-height: 41.5rem;
    }

    .section-tax-record{
        min-height: 35rem;
    }

    .section-transactions{
        min-height: 60rem;
    }
</style>
