<template>
  <div>
    <b-row class="mt-5 text-primary">
      <b-col lg="6">
        <h6>Company Details</h6>
      </b-col>
      <b-col lg="6">
        Step 2 of 2
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
    <b-form-input v-model="publicId" />
    <b-button variant="dark" to="/publicId">
      Dashboard Test
    </b-button>
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

        await this.create_seller_firm(payload)

        await this.$bvToast.toast(
          "Alright, let's get started!.",
          {
            autoHideDelay: 5000,
            variant: "success",
          }
        )
        this.buttonBusy = false

        this.$router.push(`/${ this.sellerFirm.public_id }`)


      } catch (error) {
        this.$toast.error(
          error,
          {
            autoHideDelay: 5000,
            variant: "danger",
          }
        )
        this.buttonBusy = false
      }
    },

    async create_seller_firm(payload) {
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
