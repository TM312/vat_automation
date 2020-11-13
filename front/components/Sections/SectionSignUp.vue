<template>
  <section class="my-5">
    <h6 class="text-primary">
      Get In Touch
    </h6>
    <h1>Coming in January 2021</h1>
    <p class="lead my-2">
      Feedback and continuous exchange is the best way to make a product you love. Let's start a dialogue.
    </p>
    <b-row cols="1" cols-lg="2" align-v="stretch" class="mt-5">
      <b-col cols="6" lg="5" class="px-5">
        <b-img
          src="@/assets/img/illustrations/undraw_subscribe.svg"
          center
          fluid
        />
      </b-col>
      <b-col cols="auto">
        <b-tabs pills class="mt-3">
          <b-tab title="For Amazon Sellers" active>
            <div class="mt-3">
              <p class="lead text-muted">
                If you are keen to jump on board once we release our upcoming features to
                the first users, enter your email below.
              </p>
              <form-landing-contact class="mt-5" />
            </div>
          </b-tab>
          <b-tab title="For Potential Partners">
            <div class="mt-3">
              <p class="lead text-muted">
                You are a tax consultant or service provider for
                e-commerce sellers and interested in our upcoming service?
                Get in touch and we can arrange a meeting!
              </p>
              <br />
              <code style="color:purple">
                contact@airseller.io
              </code>
            </div>
          </b-tab>
        </b-tabs>
      </b-col>
    </b-row>
  </section>
</template>

<script>
export default {
  name: "SectionSignUp",
}
</script>
