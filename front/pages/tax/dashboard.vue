<template>
    <b-container fluid>
        <dashboard-dashboard />
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


    </b-container>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        layout: "tax",
        middleware: "auth-tax",

        async fetch() {
            const { store } = this.$nuxt.context;
            if (this.countries.length == 0 || this.currencies.length == 0 || this.taxTreatments.length == 0) {
                await store.dispatch("country/get_all");
                await store.dispatch("currency/get_all");
                await store.dispatch("tax_treatment/get_all");
                await store.dispatch("utils/get_all_key_account_notifications");
            }
        },

        data() {
            return {
                checked: false
            }
        },

         computed: {
            ...mapState({
                countries: state => state.country.countries,
                currencies: state => state.currency.currencies,
                taxTreatments: state => state.tax_treatment.tax_treatments,
                notifications: state => state.utils.notifications


            })
         }

    };
</script>

<style>
</style>
