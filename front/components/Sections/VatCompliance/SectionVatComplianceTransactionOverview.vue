<template>
  <section id="vat-compliance-transaction-overview" class="py-5">
    <b-container>
      <h6 class="text-primary">
        Step 3
      </h6>
      <h1>Transaction Overview</h1>
      <p class="lead my-2">
        Get unparalleled insights by reviewing the processing of each
        individual transaction.
      </p>
    </b-container>
    <b-container fluid style="max-width: 100rem">
      <card-transaction-inputs-showcase id="neuphormism" class="my-3" />
    </b-container>
  </section>
</template>

<script>
export default {}
</script>

<style scoped>
    #neuphormism {
        border-radius: 5px;
        box-shadow: 6px 6px 12px #bdbcbc, -6px -6px 12px #ffffff !important;
    }
</style>
