<template>
  <div>
    <overview-base-data-loading v-if="$fetchState.pending && (sellerFirm.public_id != clientPublicId || sellerFirm.length === 0)" />
    <overview-base-data v-else />
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  layout: "tax-client",

  async fetch() {
    const { store } = this.$nuxt.context
    if (this.sellerFirm.length == 0 || this.sellerFirm.public_id !== this.clientPublicId) {
      await store.dispatch('seller_firm/get_by_public_id', this.clientPublicId)
    }
  },

  async asyncData({ params }) {
    const clientPublicId = params.clientPublicId
    return { clientPublicId }
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
