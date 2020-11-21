<template>
  <div class="landing">
    <section-landing-product-top class="my-3 py-5" />
    <b-container class="py-5">
      <section-testimonials class="my-5 py-5" />
      <!-- <section-supported-platforms class="my-5" /> -->
      <section-product-details class="my-5 py-5" />

      <section-why-us class="my-5" />
      <section-sign-up-all class="my-5" />
    </b-container>
  </div>
</template>

<script>
export default {
  layout: "default",
}
</script>

<style scoped>
.landing {
        max-width: 100%;
        overflow-x: hidden;
    }
</style>
