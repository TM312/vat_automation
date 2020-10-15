<template>
  <div>
    <b-tabs pills card vertical>
      <b-tab title="Overview" active>
        <b-alert :show="$dateFns.format(new Date(), 'MMMM dd, yyyy') !== $dateFns.format($auth.user.last_seen, 'MMMM dd, yyyy')" variant="primary">
          <greeting-dashboard />
        </b-alert>
        <b-row>
          <b-col cols="12" md="8" xl="9">
            <dashboard-dashboard />
          </b-col>
          <b-col cols="12" md="4" xl="3">
            <b-card title="Notifications" sub-title="Get Updates About New Clients And Your Key Accounts">
              <b-card-text v-if="notifications.length === 0">
                <div>Once you or your colleagues start inserting client data you will get notified about updates here.</div>
              </b-card-text>
              <b-card-text v-else>
                <div-notification v-for="notification in notifications" :key="notification.public_id" :notification="notification" class="my-3" />
                <hr />
              </b-card-text>
            </b-card>
          </b-col>
        </b-row>
      </b-tab>
      <b-tab title="Key Accounts" lazy>
        <div v-if="$auth.user.key_accounts.length===0">
          <b-card title="No key accounts assigned yet.">
            <b-card-text>
              <p>
                <span>You can assign clients as your key accounts by clicking on the</span>
                <b-button variant="outline-success" size="sm" class="mx-2" disabled>
                  Follow
                </b-button>
                <span>button on their profile.</span>
              </p>
              <p>These clients will appear here. Additionally you will receive notifications on any update (e.g. data uploads, etc.) concerning these clients.</p>
            </b-card-text>

            <b-button to="/tax/clients" variant="primary">
              Go to Clients
            </b-button>
          </b-card>
        </div>
        <div v-else>
          <b-row class="mb-3" cols="1" cols-lg="2" cols-xl="3">
            <b-col v-for="(client, i) in $auth.user.key_accounts" :key="i" class="mb-2">
              <card-client-short :business="client" class="mb-2" />
            </b-col>
          </b-row>
        </div>
      </b-tab>
      <b-tab v-if="$auth.user.key_accounts" title="Colleagues">
        <lazy-table-colleagues-tax />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        layout: "tax",

        async fetch() {
            const { store } = this.$nuxt.context

            if (this.countries.length === 0) {
                await store.dispatch("country/get_all")
            }

            if (this.currencies.length === 0) {
                await store.dispatch("currency/get_all")
            }

            if (this.taxTreatments.length === 0) {
                await store.dispatch("tax_treatment/get_all")
            }

            if (this.taxRateTypes.length === 0) {
                await store.dispatch("tax_rate_type/get_all")
            }

            if (this.channels.length === 0) {
                await store.dispatch("channel/get_all")
            }

            await store.dispatch("utils/get_all_key_account_notifications")
        },

        data() {
            return {
                checked: false
            }
        },

         computed: {
            ...mapState({
                channels: state => state.channel.channels,
                countries: state => state.country.countries,
                currencies: state => state.currency.currencies,
                taxTreatments: state => state.tax_treatment.tax_treatments,
                taxRateTypes: state => state.tax_rate_type.tax_rate_types,
                notifications: state => state.utils.notifications


            }),
         }

    }
</script>

<style>
</style>
