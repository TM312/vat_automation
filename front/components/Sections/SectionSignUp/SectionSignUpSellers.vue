<template>
  <section id="vat-compliance-sign-up" style="max-width: 45rem">
    <b-container align-h="center">
      <div v-if="Object.keys(subscriber).length === 0">
        <h6 class="text-primary">
          Let's Get In Touch
        </h6>
        <h3>
          Help us build a product you
          <b-icon icon="heart-fill" variant="danger" />
        </h3>

        <form-landing-contact class="my-3" feedback-on />
      </div>
      <div v-else>
        <h6 class="text-primary">
          Pleased with your interest!
        </h6>
        <h3>
          Help us build a product you
          <b-icon icon="heart-fill" variant="danger" />
        </h3>

        <div class="mt-4">
          <p class="text-muted">
            <b-icon icon="check-circle" variant="success" class="mr-2" />
            Email successfully submitted!
          </p>
          <p class="text-dark">
            We will soon start to invite users for early
            access. Contact us if there are certain features
            you need and which you couldn't find yet.
          </p>
          <code style="color:purple">service@tax-automation.com</code>
        </div>
      </div>
    </b-container>
  </section>
</template>

<script>
import { mapState } from "vuex"
export default {
  name: "SectionSignUpSellers",

  computed: {
    ...mapState({
      subscriber: (state) => state.subscriber.subscriber,
    }),
  },
}
</script>

<style>
</style>
