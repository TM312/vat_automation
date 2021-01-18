<template>
  <div class="landing">
    <section-landing-product-top class="py-5" />
    <section-testimonials class="py-5" style="background-color: #f8fbf8" />
    <!-- <section-supported-platforms class="my-5" /> -->

    <section-product-details class="py-5" />


    <section-why-us class="py-5" style="background-color: #f1f3f3" />
    <b-container class="py-5">
      <section-sign-up-all />
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
