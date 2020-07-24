<template>
    <b-container fluid>
        <b-card no-body>
            <card-greeting-dashboard />
            <dashboard-dashboard />
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

            <b-tabs content-class="mt-3">
                <b-tab title="Key Accounts" active>
                    <b-row class="mb-3" cols="1" cols-md="1" cols-lg="3" cols-xl="4">
                        <card-client-short v-for="(client, i) in $auth.user.key_accounts" :key="i" :business="client" class="mb-2" />
                    </b-row>
                </b-tab>
                <b-tab title="Colleagues">
                    <view-colleagues />
                </b-tab>
            </b-tabs>
        </b-card>
    </b-container>
</template>

<script>

    export default {
        layout: "tax",
        middleware: "auth-tax",


        data() {
            return {
                checked: false
            }
        },


        // computed: {
        //     ...mapState({
        //         accounting_firm: state => state.accounting_firm.accounting_firm
        //     }),

        //     // getCountEmployees() {
        //     //     return this.$store.getters['accounting_firm/countEmployees']
        //     //     // this.countEmployees = counter
        //     // },
        //     countEmployees() {
        //         return this.$store.getters['accounting_firm/countEmployees']
        //     },
        // },

    };
</script>

<style>
</style>
