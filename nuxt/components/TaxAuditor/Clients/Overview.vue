<template>
    <div>
        <b-row>
            <b-col cols="3">
                <card-total-count :counterNumber="countClients" subTitle="Total Number of Clients" />
            </b-col>
            <b-col cols="3">
                <card-total-count :counterNumber="countEmployees" subTitle="Total Number of Employees"/>
            </b-col>
            <b-col cols="3">
                <card-total-count :counterNumber="countClients" subTitle="Total Number of Something Else" />
            </b-col>
            <b-col cols="3">
                <card-total-count :counterNumber="countClients" subTitle="Total Number of Something Else  4th" />
            </b-col>
        </b-row>

        <hr>

        <overview-clients />

    </div>
</template>

<script>

// import { mapGetters } from 'vuex'

export default {
    name: 'Overview',
    rops: {
        self: {
            type: [Array, Object],
            required: true
        }
    },
    computed: {
        countClients() {
            return this.$store.getters['seller_firm/countClients']
        },
        countEmployees() {
            return this.$store.getters['accounting_firm/countEmployees']
        }
    },
    async fetch({ store }) {
            await store.dispatch("accounting_firm/get_by_public_id", this.self.employer_public_id);
            //await store.dispatch("seller_firm/get_clients");
        },
}
</script>

<style>

</style>
