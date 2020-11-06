<template>
  <b-button size="sm" variant="outline-primary" @click="consolelog">
    Validate
  </b-button>
</template>

<script>
export default {
  name: 'ButtonValidateTransactionInput',
  props: {
    transactionInputPublicId: {
      type: String,
      required: true
    }
  },
  methods: {
    consolelog() {
      console.log(this.transactionInputPublicId)
    }
  },

}
</script>

<style>

</style>
