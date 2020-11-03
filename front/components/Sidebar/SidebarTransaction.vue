<template>
  <b-sidebar
    id="sidebar-transaction"
    title="Transaction Details"
    right
    shadow
    width="500px"
  >
    <div class="px-3 py-2">
      <p>
        Cras mattis consectetur purus sit amet fermentum. Cras justo
        odio, dapibus ac facilisis in, egestas eget quam. Morbi leo
        risus, porta ac consectetur ac, vestibulum at eros.
      </p>
    </div>
    <div v-if="transactionPublicId !== ''" class="mt-3">
      <card-transaction-base-data :transaction="transaction" />
    </div>
    <b-button variant="primary">
      Details
    </b-button>
  </b-sidebar>
</template>

<script>

export default {
  name: "SidebarTransaction",
  props: {
    transactionPublicId: {
      type: String,
      required: true,
    }
  },

  computed: {
    transaction(){
      return this.$store.getters['transaction/getByPublicId'](this.transactionPublicId)
    }
  },

}
</script>

<style>
</style>
