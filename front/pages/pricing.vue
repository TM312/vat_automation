<template>
  <b-container class="py-5">
    <h1 class="text-dark">
      Fair Prices For Sellers of All Sizes
    </h1>
    <h2 class="text-muted mt-3">
      Start For Free
    </h2>


    <b-row>
      <b-col>
        <card-pricing-management-tool class="h-100" />
      </b-col>
      <b-col>
        <card-pricing-vat-compliance />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  layout: "default",
}
</script>
