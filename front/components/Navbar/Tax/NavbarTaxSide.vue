<template>
  <div>
    <b-nav vertical pills>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${clientPublicId}`"
        exact
      >
        Company
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${clientPublicId}/items`"
        exact
        prefetch
        :disabled="!clientPublicId"
      >
        Items
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${clientPublicId}/transactions`"
        exact
        prefetch
        :disabled="!clientPublicId"
      >
        Transactions
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${clientPublicId}/tax_records`"
        exact
        prefetch
        :disabled="!clientPublicId"
      >
        Tax Records
      </b-nav-item>
      <b-nav-item
        exact-active-class="active"
        :to="`/clients/${clientPublicId}/upload`"
        exact
        :link-class="linkClass(4)"
        :disabled="!clientPublicId"
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
    clientPublicId: {
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
