<template>
  <b-container fluid style="height: 900px">
    <b-row class="mt-5" align-h="center">
      <b-col cols="6" md="4">
        <b-card>
          <b-card-title class="text-center text-dark">
            Sign in
          </b-card-title>
          <b-card-body>
            <b-form @submit.prevent="login">
              <b-form-group id="input-group-email" label="Email" label-for="input-email">
                <b-form-input
                  id="input-email"
                  v-model="form.email"
                  type="email"
                  required
                />
              </b-form-group>

              <b-form-group id="input-group-password" label="Password" label-for="input-password">
                <b-form-input
                  id="input-password"
                  v-model="form.password"
                  type="password"
                  required
                />
              </b-form-group>

              <b-button block variant="primary" class="mt-5" type="submit">
                Continue
              </b-button>
            </b-form>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  middleware: 'guest',
  layout: 'clean',

  data() {
    return {
      showPassword: false,
      form: {
        email: '',
        password: '',
      },
    }
  },
  methods: {
    async login() {
      const payload = {
        email: this.form.email,
        password: this.form.password,
        u_type: 'admin'
      }
      try {
        await this.$auth.loginWith('local', {
          data: payload,
        })

        this.$router.push('/dashboard')

      } catch (err) {
        // console.log('ERRRORCODE')
        // console.log(err.response.status)
        const status = err.response.status
        if (status === 401 || status === 404) {
          this.$bvToast.toast('Invalid password or email.', {
            autoHideDelay: 5000,
            variant: 'danger'
          })
        } else {
          this.$bvToast.toast('There seems to be a problem. Please try again later.', {
            autoHideDelay: 5000,
            variant: 'danger'
          })
        }
      }
    },
  },
}
</script>
