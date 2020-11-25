<template>
  <section id="vat-compliance-sign-up">
    <b-container align-h="center">
      <b-card v-if="Object.keys(subscriber).length === 0">
        <h6 class="text-primary">
          Let's Get In Touch
        </h6>
        <h3>
          Help us build a product you
          <b-icon icon="heart-fill" variant="danger" />
        </h3>

        <form-landing-contact class="my-4" feedback-on />
      </b-card>
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
            We will soon start to invite users for early access.
            Is there any feature you need to are looking for and which you couldn't find yet. Tell us and we can build it.
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
