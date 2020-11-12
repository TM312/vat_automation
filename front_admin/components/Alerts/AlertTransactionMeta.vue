<template>
  <b-alert>
    <span>
      This transaction was modified at {{ transaction.modified_at }}
    </span>
    <span v-if="transaction.modified_by">
      by {{ transaction.modified_by }}
    </span>
    <span>.</span>
  </b-alert>
</template>

<script>
export default {
  name: 'AlertTransactionMeta',

  props: {
    transaction: {
      type: Object,
      required: true
    }
  }

}
</script>

<style>

</style>
