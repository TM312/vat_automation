<template>
  <b-card>
    <b-card-title>
      Vat Compliance
      <badge-coming-soon class="ml-1" />
    </b-card-title>
    <b-card-sub-title>VAT Registrations &amp; Filings</b-card-sub-title>
    <b-card-text class="py-3">
      <b-tabs>
        <b-tab title="Standard" active class="pt-3 h-100">
          <b-container class="justify-content-center my-5">
            <b-row align-v="center">
              <b-col>
                <h1 class="text-dark text-right">
                  {{ value }} €
                </h1>
              </b-col>
              <b-col>
                <h5 class="text-muted">
                  <span v-show="!panEU">per country <br /></span>
                  {{ annually ? "per year" : "per month" }}
                </h5>
              </b-col>
            </b-row>
          </b-container>
          <div>
            <b-form-checkbox
              v-model="annually"
              name="check-button"
              switch
            >
              <span
                :class="
                  annually ? 'text-primary' : 'text-muted'
                "
              >
                Pay Annually
              </span>
              <b-badge
                :variant="annually ? 'warning' : 'secondary'"
                pill
                class="ml-1"
              >
                Save 20%
              </b-badge>
            </b-form-checkbox>
          </div>
          <div>
            <b-form-checkbox
              v-model="panEU"
              name="check-button"
              switch
            >
              <span
                :class="panEU ? 'text-primary' : 'text-muted'"
              >
                Amazon PAN EU (DE, ES, FR, IT, PL, CZ, GB)
              </span>
            </b-form-checkbox>
          </div>
        </b-tab>
        <b-tab title="Enterprise" class="py-3 h-100" disabled>
          <b-card
            bg-variant="dark"
            text-variant="light"
            title="Design a custom package for your business"
          >
            Available for businesses with large payments volume or
            unique business models
          </b-card>
        </b-tab>
      </b-tabs>
      <div class="mt-5">
        <p class="text-muted">
          <b-icon
            icon="check"
            variant="success"
            class="mr-1"
          />
          Everything you need to stay vat compliant in all
          PAN-EU countries.
        </p>
      </div>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: "CardPricingVatCompliance",

  data() {
    return {
      annually: false,
      panEU: false,
      numberCountries: 1,
    }
  },

  computed: {
    value() {
      if (!this.panEU) {
        const value = 60 * this.numberCountries
        return this.annually ? value * 0.8 * 12 : value
      } else {
        const value = 500
        return this.annually ? value * 0.8 * 12 : value
      }
    },
  },
}
</script>

<style>
</style>
