<template>
  <div>
    <b-container class="py-5">
      <b-jumbotron bg-variant="transparent" text-variant="dark" header="Building with Sellers' in Mind">
        <template #lead class="text-secondary mt-5">
          <h4 class="text-info">
            Explore The Interactive Demo
          </h4>

          Tax-Automation is a technology company that that builds economic infrastructure for the internet.
          Businesses of every size—from new startups to public
          companies—use our software to accept payments and manage their businesses online.

          We believe sustainable, organic growth is the best way to build a lasting company.

          <hr />

          Hi! I'm Derrick Reimer, the founder of SavvyCal.
          Our mission is to cut the friction and awkwardness out of scheduling time with people.

          We’re an indie SaaS company with a little bit of financial backing from TinySeed.
          We believe sustainable, organic growth is the best way to build a lasting company.

          Previously, I was the co-founder of Drip. I host a weekly podcast called The Art of Product.

          <hr />

          <h2>sellerFirm fetched? {{ !!sellerFirm }}</h2>
        </template>
      </b-jumbotron>
    </b-container>

    <b-container v-if="!$fetchState.pending">
      <section-vat-compliance-data-upload v-if="!$fetchState.pending" class="py-5" />

      <section-vat-compliance-company-information v-if="!$fetchState.pending" class="py-5" />
    </b-container>

    <b-container v-if="!$fetchState.pending" fluid>
      <section-vat-compliance-transaction-overview v-if="!$fetchState.pending" class="py-5" />
    </b-container>

    <b-container>
      <section-vat-compliance-tax-records v-if="!$fetchState.pending" />

      <section
        id="vat-compliance-sign-up"
        style="max-width: 45rem"
        class="my-5"
        background="light"
      >
        <b-container align-h="center">
          <h6 class="text-primary">
            Let's Get In Touch
          </h6>
          <h3>Help us building a product you love.</h3>
          <form-landing-contact class="my-3" feedback-on />
        </b-container>
      </section>
    </b-container>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  layout: "default",

  async fetch() {
    const { store } = this.$nuxt.context

    if (this.sellerFirm.length === 0) {
      await store.dispatch("seller_firm/get_sample")
    }

    if (this.countries.length === 0) {
      await store.dispatch("country/get_all")
    }

    if (this.currencies.length === 0) {
      await store.dispatch("currency/get_all")
    }

    if (this.taxTreatments.length === 0) {
      await store.dispatch("tax_treatment/get_all")
    }

    if (this.taxRateTypes.length === 0) {
      await store.dispatch("tax_rate_type/get_all")
    }

    if (this.channels.length === 0) {
      await store.dispatch("channel/get_all")
    }

    if (this.vatThresholds.length === 0) {
      await store.dispatch("vat_threshold/get_all")
    }

    if (this.transactionInputs.length === 0) {
      await store.dispatch("transaction_input/get_sample")
    }


  },

  computed: {
    ...mapState({
      sellerFirm: state => state.seller_firm.seller_firm,
      channels: state => state.channel.channels,
      countries: state => state.country.countries,
      currencies: state => state.currency.currencies,
      taxTreatments: state => state.tax_treatment.tax_treatments,
      taxRateTypes: state => state.tax_rate_type.tax_rate_types,
      vatThresholds: state => state.vat_threshold.vat_thresholds,
      transactionInputs: state => state.transaction_input.transaction_inputs

    })
  },

}
</script>

<style>
</style>
