<template>
    <div>
        channels.length: {{ channels.length }} <br>
        countries.length: {{ countries.length }} <br>
        currencies.length: {{ currencies.length }} <br>
        taxTreatments.length: {{ taxTreatments.length }} <br>
        taxRateTypes.length: {{ taxRateTypes.length }} <br>
        notifications.length: {{ notifications.length }} <br>
        <b-tabs pills card vertical>
            <b-tab title='Overview' active>
                <b-row>
                    <b-col cols="12" md="8" xl="9">
                        <dashboard-dashboard />
                        <card-greeting-dashboard v-once class="mx-3" />
                    </b-col>
                    <b-col cols="auto">
                        <card-notification v-for="notification in notifications" :key="notification.public_id" :notification="notification"  class="my-3" />
                    </b-col>
                </b-row>
            </b-tab>
            <b-tab title='Key Accounts' lazy>
                <div v-if="$auth.user.key_accounts.length===0">
                    <b-card title="No key accounts assigned yet.">
                        <b-card-text>
                            <p>
                                <span>You can assign clients as your key accounts by clicking on the</span>
                                <b-button variant="outline-success" size="sm" class="mx-2" disabled>Follow</b-button>
                                <span>button on their profile.</span>
                            </p>
                            <p>These clients will appear here. Additionally you will receive notifications on any update (e.g. data uploads, etc.) concerning these clients.</p>
                        </b-card-text>

                        <b-button to="/tax/clients" variant="primary">Go to Clients</b-button>

                    </b-card>
                </div>
                <div v-else>
                    <b-row class="mb-3" cols="1" cols-lg="2" cols-xl="3">
                        <b-col class="mb-2" v-for="(client, i) in $auth.user.key_accounts" :key="i">
                            <card-client-short :business="client" class="mb-2" />
                        </b-col>
                    </b-row>
                </div>
            </b-tab>
            <b-tab title="Colleagues" v-if="$auth.user.key_accounts">
                <lazy-table-colleagues-tax />
            </b-tab>
        </b-tabs>
    </div>


    <!-- <b-container fluid>
        <dashboard-dashboard class="mt-2" />
        <card-greeting-dashboard class="mx-3" />
        <br>

        <b-row>
            <b-col cols="6" md="8" xl="9">
                <b-tabs content-class="mt-3">
                    <b-tab title="Key Accounts" active>
                        <b-row class="mb-3" cols="1" cols-lg="2" cols-xl="3">
                            <b-col class="mb-2" v-for="(client, i) in $auth.user.key_accounts" :key="i">
                                <card-client-short :business="client" class="mb-2" />
                            </b-col>
                        </b-row>
                    </b-tab>
                    <b-tab title="Colleagues">
                        <lazy-table-colleagues-tax />
                    </b-tab>
                </b-tabs>
            </b-col>
            <b-col cols="6" md="4" xl="3">
                <card-notification v-for="notification in notifications" :key="notification.public_id" :notification="notification"  class="my-3" />
            </b-col>

        </b-row>


    </b-container> -->
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        layout: "tax",

        async fetch() {
            const { store } = this.$nuxt.context;
            if (this.countries.length == 0) {
                await store.dispatch("country/get_all");
            }

            if (this.currencies.length == 0) {
                await store.dispatch("currency/get_all");
            }

            if (this.taxTreatments.length == 0) {
                await store.dispatch("tax_treatment/get_all")
            }

            if (this.taxRateTypes.length == 0) {
                await store.dispatch("tax_rate_type/get_all");
            }

            if (this.channels.length == 0) {
                await store.dispatch("channel/get_all");
            }

            await store.dispatch("utils/get_all_key_account_notifications");
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


            })
         }

    };
</script>

<style>
</style>
