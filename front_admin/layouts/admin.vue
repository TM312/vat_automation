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

    // await store.dispatch("utils/get_all_key_account_notifications")
  },


  computed: {
    ...mapState({
      channels: state => state.channel.channels,
      countries: state => state.country.countries,
      currencies: state => state.currency.currencies,
      taxTreatments: state => state.tax_treatment.tax_treatments,
      taxRateTypes: state => state.tax_rate_type.tax_rate_types,
      vatThresholds: state => state.vat_threshold.vat_thresholds,


      //   notifications: state => state.utils.notifications


    })
  }

}
</script>
