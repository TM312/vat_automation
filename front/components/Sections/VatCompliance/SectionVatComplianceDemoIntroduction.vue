<template>
  <section>
    <b-row>
      <b-col>
        <h3 class="text-info">
          We have prepared a small demo that will provide you a good idea how this process works.
        </h3>
        <card-sample-test class="mt-5 sizing" />
      </b-col>
      <b-col />
    </b-row>
  </section>
</template>

<script>
export default {
  name: "SectionVatComplianceDemoIntroduction",
}
</script>

<style scoped>
    .sizing {
        min-width: 30rem;
        max-width: 50rem;
    }
</style>
