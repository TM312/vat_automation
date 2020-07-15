<template>
<div>
        <h1>{{ greeting }}</h1>
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

        async fetch() {
            const { store } = this.$nuxt.context
            await store.dispatch("accounting_firm/get_by_public_id", this.tax_auditor.employer_public_id);
        },

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

        created() {
            this.tax_auditor = this.$auth.user;
            this.nowHours = new Date().getHours()
        },

        computed: {
            greeting: function() {
                if (this.nowHours <= 5) {
                    return `Good Morning or Good Night, ${ this.tax_auditor.name } ?`
                } else if (6 <= this.nowHours && this.nowHours <= 11) {
                    return `Good Morning, ${ this.tax_auditor.name } !`
                } else if (12 <= this.nowHours && this.nowHours <= 14) {
                    return `Happy Lunch Time, ${ this.tax_auditor.name } !`
                } else if (15 <= this.nowHours && this.nowHours <= 17) {
                    return `Good Afternoon, ${ this.tax_auditor.name } !`
                } else {
                    return `Good Evening, ${ this.tax_auditor.name } !`
                }
            }
        },


    };
</script>

<style>
</style>
