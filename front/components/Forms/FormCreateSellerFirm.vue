<template>
  <div>
    <b-row class="mt-5 text-primary">
      <b-col lg="6">
        <h6>Company Details</h6>
      </b-col>
      <b-col lg="6">
        Step 1 of 2
      </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col lg="6">
        <div class="mb-4">
          <b-form-group
            id="input-group-company-name"
            label="Company Name"
            label-for="input-company-name"
          >
            <b-form-input
              id="input-company-name"
              v-model="form.name"
              type="text"
              required
            />
          </b-form-group>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col lg="6">
        <div>
          <b-form-group
            id="input-group-input-establishment-country"
            label="Establishment Country"
            label-for="input-establishment-country"
          >
            <b-form-select
              id="input-establishment-country"
              v-model="form.establishment_country_code"
              :options="optionsCountryCode"
            />
          </b-form-group>
        </div>
      </b-col>
      <b-col lg="6">
        <p class="text-muted">
          Country Suggestions
        </p>
        <b-button
          v-for="(code, index) in countryShortList"
          :key="index"
          size="sm"
          variant="outline-primary"
          class="mr-1"
          @click="form.establishment_country_code = code"
          @pressed="form.establishment_country_code === code"
        >
          {{ code }}
        </b-button>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-button
          variant="primary"
          :disabled="validationSubmit"
          class="mt-3"
          pill
          @click="submitPayload()"
        >
          <span class="px-5">
            Next
            <b-icon icon="arrow-right-short" class="ml-1" />
          </span>
        </b-button>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "FormAddSellerFirm",

  props: {
    registered: {
      type: Boolean,
      required: false,
      default: true,
    },
  },

  data() {
    return {
      countryShortList: ['AT', 'BE', 'CH', 'CZ', 'DE', 'ES', 'FR', 'IT', 'PL', 'US'],
      publicId: null,
      buttonBusy: false,
      form: {
        name: null,
        establishment_country_code: null,
      },
    }
  },

  computed: {
    ...mapState({
      countries: (state) => state.country.countries,
      seller: (state) => state.seller.seller,
      sellerFirm: state => state.seller_firm.seller_firm
    }),

    optionsCountryCode() {
      let options = this.countries.map((country) => {
        let properties = {
          value: country.code,
          text: country.name,
        }
        return properties
      })
      return options
    },

    validationSubmit() {
      if (
        this.form.name !== null &&
                    this.form.establishment_country_code !== null &&
                    !this.buttonBusy
      ) {
        return false
      } else {
        return true
      }
    },
  },

  methods: {
    async submitPayload() {
      this.buttonBusy = true

      const payload = {
        name: this.form.name,
        establishment_country_code: this.form.establishment_country_code,
        user_public_id: this.seller.public_id
      }
      try {

        await this.createSellerFirm(payload)

        this.$bvToast.toast(

          'Great! Already half the way!',
          {
            title: 'Seller Account Created',
            autoHideDelay: 5000,
            variant: 'success'
          }
        )

        this.buttonBusy = false

        this.$emit('next')



      } catch (error) {
        this.$bvToast.toast(
          error,
          {
            title: 'Oops and error',
            autoHideDelay: 5000,
            variant: "danger",
          }
        )
        this.buttonBusy = false
      }
    },

    async createSellerFirm(payload) {
      await this.$store.dispatch(
        "seller_firm/create",
        payload
      )
    },

  },
}
// async register() {
//       const payload = {
//         email: this.form.email,
//         password: this.form.password
//       }
//       try {
//         await createSeller(payload)

//         // await this.$auth.loginWith('local', {
//         //   data: payload
//         // })


//         // this.$router.push('/dashboard')


</script>
