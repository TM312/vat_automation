<template>
    <b-container fluid>
        <dashboard-dashboard />
        <card-greeting-dashboard class="mx-3" />
        <br>
        <b-row>
            <b-col cols="3">
            </b-col>
            <b-col cols="3">
            </b-col>
            <b-col cols="3">
                <!-- <card-total-count :counterNumber="0" subTitle="Total Number of Something Else" /> -->
            </b-col>
            <b-col cols="3">
                <!-- <card-total-count :counterNumber="0" subTitle="Total Number of Something Else  4th" /> -->
            </b-col>
        </b-row>

        <b-tabs content-class="mx-3">
            <b-tab title="Key Accounts" active>
                <b-row class="my-3" cols="1" cols-md="1" cols-lg="3" cols-xl="4">
                    <card-client-short v-for="(client, i) in $auth.user.key_accounts" :key="i" :business="client" class="mb-2" />
                </b-row>
            </b-tab>
            <b-tab title="Colleagues">
                <lazy-table-colleagues-tax />
            </b-tab>
        </b-tabs>
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
                taxTreatments: state => state.tax_treatment.tax_treatments

            })
         }

    };
</script>

<style>
</style>
