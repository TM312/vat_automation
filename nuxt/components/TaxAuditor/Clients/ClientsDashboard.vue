<template>
    <div>
        <b-row>
            <b-col cols="3">
                <card-total-count-function :counterFunction="countEmployees" subTitle="Total Number of Employees" />
            </b-col>
            <b-col cols="3">
                <card-total-count-function :counterFunction="countClients" subTitle="Total Number of Clients" />
            </b-col>
            <b-col cols="3">
                <card-total-count-function :counterFunction="countClients" subTitle="Total Number of Something Else" />
            </b-col>
            <b-col cols="3">
                <card-total-count-function :counterFunction="countClients" subTitle="Total Number of Something Else  4th" />
            </b-col>
        </b-row>
    </div>
</template>

<script>
export default {
    name: 'ClientsDashboard',

    methods: {
        countClients() {
            return this.$store.getters['accounting_firm/countClients']
        },
        countEmployees() {
            return this.$store.getters['accounting_firm/countEmployees']
        },
    }
}
</script>

<style>

</style>
