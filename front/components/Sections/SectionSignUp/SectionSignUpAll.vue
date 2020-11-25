<template>
  <section class="my-5">
    <h6 v-if="Object.keys(subscriber).length === 0" class="text-primary">
      Beam Me Up
    </h6>
    <h6 v-else class="text-primary">
      Pleased With Your Interest
    </h6>
    <h1>Coming In January 2021</h1>
    <p class="lead my-2">
      Continuous feedback is the best way to build a product you
      <b-icon icon="heart-fill" variant="danger" /> Let's start a
      dialogue.
    </p>
    <b-row cols="1" cols-lg="2" align-v="stretch" class="mt-5">
      <b-col cols="6" lg="5" class="px-5">
        <spaceship-beam />
      </b-col>
      <b-col cols="auto">
        <b-card v-if="Object.keys(subscriber).length === 0">
          <b-tabs pills class="mt-3">
            <b-tab title="For Amazon Sellers" active>
              <div
                v-if="Object.keys(subscriber).length === 0"
                class="mt-3"
              >
                <p class="text-muted">
                  Enter your email for early access and updates.
                </p>
                <form-landing-contact class="mt-2" />
              </div>
              <div v-else class="mt-4">
                <p class="text-muted">
                  <b-icon
                    icon="check-circle"
                    variant="success"
                    class="mr-2"
                  />
                  Email successfully submitted!
                </p>
                <p class="text-dark">
                  We will soon start to invite users for early access.
                  Is there any feature you need to are looking for and which you couldn't find yet on our
                  <nuxt-link to="/vat-compliance">
                    product page
                  </nuxt-link>? Tell us and we can build it.
                </p>
                <code style="color: purple">
                  service@tax-automation.com
                </code>
              </div>
            </b-tab>
            <b-tab title="For Potential Partners">
              <div class="my-3">
                <p class="text-muted">
                  If you are a tax consultant or service provider
                  for e-commerce sellers and interested in a
                  collaboration? Get in touch! We would love to
                  hear from you.
                </p>
                <code style="color: purple">
                  contact@tax-automation.com
                </code>
              </div>
            </b-tab>
          </b-tabs>
        </b-card>
      </b-col>
    </b-row>
  </section>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "SectionSignUpAll",
  computed: {
    ...mapState({
      subscriber: (state) => state.subscriber.subscriber,
    }),
  },
}
</script>
