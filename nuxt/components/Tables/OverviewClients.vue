<template>
    <b-tabs content-class="mt-3">
        <b-tab title="Card View" active>
            <b-row cols="3" md="4">
                <card-client-short v-for="(client_seller_firm, i) in client_seller_firms" :key="i" :business="client_seller_firm" />
            </b-row>
        </b-tab>
        <b-tab title="Table View" disabled>
            <p>tbd</p>
            <!-- <AddDistanceSalesFiles /> -->
        </b-tab>
    </b-tabs>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        name:'OverviewClients',

        computed: {
            ...mapState({
                client_seller_firms: state => state.seller_firm.client_seller_firms
            }),
        }
    }
</script>

<style>
</style>
