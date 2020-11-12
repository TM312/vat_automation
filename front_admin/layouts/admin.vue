<template>
  <div>
    <navbar-admin />
    <b-container fluid>
      <h3 class="text-muted text-center my-3">
        Admin Area
      </h3>
      <nuxt class="my-5" />
    </b-container>
    <Footer />
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  middleware: 'auth',

  async fetch() {
    const { store } = this.$nuxt.context

    if (this.platforms.length === 0) {
      await store.dispatch("platform/get_all")
    }

    if (this.eu.length === 0) {
      // https://stackoverflow.com/questions/23593052/format-javascript-date-as-yyyy-mm-dd
      var todayDate = new Date().toISOString().slice(0,10)
      await store.dispatch("country/get_eu_by_date", todayDate)
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

    if (this.transaction_type.length === 0) {
      await store.dispatch("transaction_type/get_all")
    }

    if (this.transaction_type_public.length === 0) {
      await store.dispatch("transaction_type_public/get_all")
    }

    // await store.dispatch("utils/get_all_key_account_notifications")
  },


  computed: {
    ...mapState({
      eu: state => state.country.eu,
      platforms: state => state.platform.platforms,
      channels: state => state.channel.channels,
      countries: state => state.country.countries,
      currencies: state => state.currency.currencies,
      taxTreatments: state => state.tax_treatment.tax_treatments,
      taxRateTypes: state => state.tax_rate_type.tax_rate_types,
      vatThresholds: state => state.vat_threshold.vat_thresholds,
      transactionTypes: state => state.transaction_type.transaction_types,
      transactionTypePublics: state => state.transaction_type_public.transaction_type_publics,


      //   notifications: state => state.utils.notifications


    })
  }

}
</script>
