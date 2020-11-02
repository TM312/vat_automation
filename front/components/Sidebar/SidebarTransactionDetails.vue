<template>
  <div>
    <h2>hi</h2>
    <card-transaction-base-data :transaction="transaction" />
  </div>
</template>

<script>
export default {
  name: 'SidebarTransactionDetails',
  props: {
    transaction: {
      type: [Object, Array],
      required: true
    }
  }

}
</script>

<style>

</style>
