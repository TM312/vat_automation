<template>
<div>
        <card-greeting-dashboard />
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

        <view-colleagues />

    </div>

</template>

<script>
    // import { mapState } from 'vuex'

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
