<template>
  <section>
    <b-container>
      <h5 style="color: purple">
        VAT Compliance
      </h5>
      <h1>A platform designed to meet your VAT requirements with ease</h1>
      <p class="lead mt-3">
        Calculate your VAT and file your turnover tax advance return
        within minutes. Our solution provides you with transparency over
        your sales, their tax implications and distance selling
        thresholds at an unprecedented level of detail.
      </p>
      <span class="mt-2">
        <button-enter-arrow-right
          to="/register"
          content="Get Started"
        />
        <button-enter-arrow-right
          to="/contact"
          content="Contact Us"
          variant="link"
        />
      </span>
    </b-container>
    <b-container class="py-5">
      <b-card
        border-variant="info"
        title="Interactive Demo"
        sub-title="We have prepared a small demo that lets you get a feeling of our platform."
      >
        <b-card-text>
          We have prepared a small demo that will provide you a good
          idea how this process works.
        </b-card-text>
      </b-card>
    </b-container>
  </section>
</template>

<script>
export default {
  name: "SectionVatComplianceTop",
}
</script>

<style>
</style>
