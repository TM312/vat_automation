<template>
  <b-container fluid>
    <b-row class="mt-5">
      <b-col lg="6">
        <h2>All the benefits</h2>
      </b-col>
      <b-col lg="6">
        <h1>Register</h1>
        <div>
          <b-form @submit.prevent="register">
            <b-form-group
              id="input-group-email"
              label="Email address:"
              label-for="input-email"
            >
              <b-form-input
                id="input-email"
                v-model="form.email"
                type="email"
                :state="validation_email"
                required
              />
            </b-form-group>
            <b-form-group
              id="input-group-password"
              label="Password:"
              label-for="input-password"
            >
              <b-form-input
                id="input-password"
                v-model="form.password"
                type="password"
                :state="validation_pw"
                required
              />
              <b-form-invalid-feedback :state="validation_pw">
                The chosen password is too short.
              </b-form-invalid-feedback>
              <b-form-valid-feedback :state="validation_pw">
                Looks Good.
              </b-form-valid-feedback>
            </b-form-group>
            <b-form-group
              id="input-group-password"
              label="Repeat password:"
              label-for="input-password"
            >
              <b-form-input
                id="input-password2"
                v-model="form.password2"
                type="password"
                :state="validation_repeatpw"
                required
              />
              <b-form-invalid-feedback :state="validation_repeatpw">
                The two passwords do not match.
              </b-form-invalid-feedback>
              <b-form-valid-feedback :state="validation_repeatpw">
                Looks Good.
              </b-form-valid-feedback>
            </b-form-group>
            <b-button
              type="submit"
              variant="primary"
              :disabled="validation_submit"
            >
              Create your account
            </b-button>
          </b-form>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
// import axios from '~/plugins/axios'
export default {
  middleware: 'guest',
  data() {
    return {
      showPassword: false,
      form: {
        email: '',
        password: '',
        password2: ''
      }
    }
  },
  computed: {
    validation_email() {
      if (this.form.email.length > 3) {
        /* eslint-disable */
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return re.test(String(this.form.email).toLowerCase())
      } else {
        return null
      }
    },
    validation_pw() {
      if (this.form.password.length > 0) {
        return this.form.password.length >= 8
      } else {
        return null
      }
    },
    validation_repeatpw() {
      if (this.form.password2.length > 0) {
        return this.form.password2 == this.form.password
      } else {
        return null
      }
    },
    validation_submit() {
      if (this.validation_pw && this.validation_repeatpw) {
        return false
      } else {
        return true
      }
    }
  },
  methods: {
    async register() {
      const payload = {
        email: this.form.email,
        password: this.form.password
      }
      try {
        await this.$axios.post('/user/self', payload)

        await this.$auth.loginWith('local', {
          data: payload
        })

        // this.$bvToast.toast('Logging in', {
        //   title: 'Logger',
        //   variant: 'primary'
        // })

        this.$router.push('/dashboard')

        this.$toast.success('Successfully registered! Welcome!', {
          duration: 5000
        })
      } catch (err) {
        const status = err.response.status
        if (status === 409) {
          console.log('status check')

          this.$toast.error(
            'A user with this email adress already exists. Try logging in instead.',
            { duration: 5000 }
          )
        } else if (status === 401 || status === 404) {
          this.$toast.error('Invalid password or email.', { duration: 5000 })
        } else {
          this.$toast.error(
            'There seems to be a problem signing you in. Please try again later.',
            { duration: 5000 }
          )
        }
      }
    }
  }
}
</script>
