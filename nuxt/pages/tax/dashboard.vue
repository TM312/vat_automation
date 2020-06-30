<template>
<div>
        <b-row>
            <b-col cols="3">
                <!-- <card-total-count :counterNumber="countEmployees" subTitle="Total Number of Colleagues" /> -->

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

        <view-colleagues />

    </div>

</template>

<script>
    // import { mapState } from 'vuex'

    export default {
        layout: "tax",
        middleware: "auth-tax",

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch("accounting_firm/get_by_public_id", this.tax_auditor.employer_public_id);
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

        created() {
            this.tax_auditor = this.$auth.user;
        }


    };
</script>

<style>
</style>
