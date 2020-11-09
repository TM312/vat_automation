<template>
  <div>
    <b-nav vertical pills>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${sellerFirmPublicId}`"
        exact
      >
        Company
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${sellerFirmPublicId}/items`"
        exact
        prefetch
        :disabled="!sellerFirmPublicId"
      >
        Items
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${sellerFirmPublicId}/transactions`"
        exact
        prefetch
        :disabled="!sellerFirmPublicId"
      >
        Transactions
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${sellerFirmPublicId}/tax-records`"
        exact
        prefetch
        :disabled="!sellerFirmPublicId"
      >
        Tax Records
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${sellerFirmPublicId}/upload`"
        exact
        :link-class="linkClass(4)"
        :disabled="!sellerFirmPublicId"
      >
        Upload Files
      </b-nav-item>
    </b-nav>
  </div>
</template>

<script>
export default {
  name: "NavbarTaxSide",
  props: {
    sellerFirmPublicId: {
      default: null,
      type: String,
      required: false,
    },
  },
  methods: {
    linkClass(idx) {
      if (this.tabIndex === idx) {
        return ["bg-info", "text-info"]
      } else {
        return ["bg-light", "text-info"]
      }
    },
  },
}
</script>

<style>
</style>
