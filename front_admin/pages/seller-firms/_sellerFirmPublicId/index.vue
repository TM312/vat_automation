<template>
  <div>
    <overview-base-data-loading v-if="$fetchState.pending && (sellerFirm.public_id != sellerFirmPublicId || sellerFirm.length === 0)" />
    <overview-base-data v-else />
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  layout: "admin-seller-firm",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.sellerFirm.length == 0 || this.sellerFirm.public_id !== this.sellerFirmPublicId) {
      await store.dispatch('seller_firm/get_by_public_id', this.sellerFirmPublicId)
    }
  },

  async asyncData({ params }) {
    const sellerFirmPublicId = params.sellerFirmPublicId
    return { sellerFirmPublicId }
  },


  computed: {
    ...mapState({
      sellerFirm: state => state.seller_firm.seller_firm
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

<style></style>
