<template>
  <div>
    <overview-base-data-loading v-if="$fetchState.pending && (sellerFirm.public_id != sellerFirmPublicId || sellerFirm.length === 0)" />
    <overview-base-data v-else />
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  layout: "tax-client",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.sellerFirm.length == 0 || this.sellerFirm.public_id !== this.sellerFirmPublicId) {
      await store.dispatch('seller_firm/get_by_public_id', this.sellerFirmPublicId)
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

    // await store.dispatch("utils/get_all_key_account_notifications")
  },

  async asyncData({ params }) {
    const sellerFirmPublicId = params.sellerFirmPublicId
    return { sellerFirmPublicId }
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


    //   notifications: state => state.utils.notifications
    })
  },

  methods: {
    linkClass(idx) {
      if (this.tabIndex === idx) {
        return ['bg-info', 'text-info']
      } else {
        return ['bg-light', 'text-info']
      }
    }

  },
}
</script>



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

    await store.dispatch("utils/get_all_key_account_notifications")
  },

  data() {
    return {
      checked: false
    }
  },

  computed: {
    ...mapState({
      channels: state => state.channel.channels,
      countries: state => state.country.countries,
      currencies: state => state.currency.currencies,
      taxTreatments: state => state.tax_treatment.tax_treatments,
      taxRateTypes: state => state.tax_rate_type.tax_rate_types,
      vatThresholds: state => state.vat_threshold.vat_thresholds,


      notifications: state => state.utils.notifications


    }),
  }

}
