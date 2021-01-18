<template>
  <div>
    <b-row class="mt-5 text-primary">
      <b-col lg="6">
        <h6>Account Details</h6>
      </b-col>
      <b-col lg="6">
        Step 2 of 2
      </b-col>
    </b-row>
    <b-row class="mt-3">
      <b-col lg="6">
        <b-form @submit.prevent="register">
          <b-form-group id="input-group-name" label="Display Name" label-for="input-name" class="mb-4">
            <b-form-input
              id="input-name"
              v-model="form.name"
              required
              @input="inputField = 'name'"
            />
          </b-form-group>

          <b-form-group id="input-group-email" label="Email" label-for="input-email" class="mb-4">
            <b-form-input
              id="input-email"
              v-model="form.email"
              type="email"
              :state="validationEmail"
              required
              @input="inputField = 'email'"
            />
          </b-form-group>

          <b-form-group id="input-group-password" label="Password" label-for="input-password">
            <b-form-input
              id="input-password"
              v-model="form.password"
              type="password"
              :state="validationPw"
              required
              @input="inputField = 'password'"
            />
            <b-form-invalid-feedback :state="validationPw">
              The chosen password is too short.
            </b-form-invalid-feedback>
            <b-form-valid-feedback :state="validationPw">
              Looks Good.
            </b-form-valid-feedback>
          </b-form-group>

          <b-form-group id="input-group-password" label="Repeat Password" label-for="input-password">
            <b-form-input
              id="input-password2"
              v-model="form.password2"
              type="password"
              :state="validationRepeatPw"
              required
              @input="inputField = 'password2'"
            />
            <b-form-invalid-feedback :state="validationRepeatPw">
              The two passwords do not match.
            </b-form-invalid-feedback>
            <b-form-valid-feedback :state="validationRepeatPw">
              Looks Good.
            </b-form-valid-feedback>
          </b-form-group>

          <b-button
            variant="primary"
            type="submit"
            :disabled="validationSubmit"
            class="mt-3"
            pill
          >
            <span class="px-5">
              Next
              <b-icon icon="arrow-right-short" class="ml-1" />
            </span>
          </b-button>
        </b-form>
        <div class="mt-2">
          <small class="text-muted">
            You already have an account? Try to <nuxt-link to="/login">
              log in
            </nuxt-link> instead.
          </small>
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  middleware: 'guest',
  data() {
    return {
      showPassword: false,
      inputField: '',
      form: {
        name: '',
        email: '',
        password: '',
        password2: ''
      },
    }
  },
  computed: {
    ...mapState({
      sellerFirm: (state) => state.seller_firm.seller_firm
    }),

    validationEmail() {
      if (this.form.email.length > 3) {
        /* eslint-disable */
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return re.test(String(this.form.email).toLowerCase())
      } else {
        return null
      }
    },

    validationPw() {
      if (this.form.password.length > 3) {
        return this.form.password.length >= 8
      } else {
        return null
      }
    },
    validationRepeatPw() {
      if (this.form.password2.length > 0 && this.form.password2.length == this.form.password.length) {
        return this.form.password2 == this.form.password
      } else {
        return null
      }
    },
    validationSubmit() {
      if (this.validationPw && this.validationRepeatPw) {
        return false
      } else {
        return true
      }
    }
  },
  methods: {
    async createSeller(payload) {
        const { store } = this.$nuxt.context
        await store.dispatch('seller/create', payload)
    },

    async updateSellerFirm() {
        const { store } = this.$nuxt.context
        const payload = [this.sellerFirm.public_id, {}]
        await store.dispatch('seller_firm/update', payload)
    },

    async register() {
      const payload = {
        name: this.form.name,
        email: this.form.email,
        password: this.form.password,
        role: 'admin',
        employer_public_id: this.sellerFirm.public_id,
      }

      try {
        await this.createSeller(payload)



        await this.$bvToast.toast(
                "Alright, let's get started!.",
                {
                    title: 'Seller Firm Registered',
                    autoHideDelay: 5000,
                    variant: "success",
                }
                )



        const loginPayload = {
            email: this.form.email,
            password: this.form.password,
            u_type: 'seller'
        }

        await this.$auth.loginWith('local', { data: loginPayload })

        await this.updateSellerFirm()

        this.$router.push('/dashboard')



      } catch (err) {
        const status = err.response.status
        if (status === 409) {

          this.$bvToast.toast(
            'A user with this email adress already exists. Try logging in instead.',
            { autoHideDelay: 5000, variant:"danger" }
          )
        } else if (status === 401 || status === 404) {
          this.$bvToast.toast(
            'Invalid password or email.',
            { autoHideDelay: 5000, variant:"danger" }
            )
        } else {
          this.$bvToast.toast(
            err.description,
            { autoHideDelay: 5000, variant:"danger" }
          )
        }
      }
    }
  }
}
</script>
