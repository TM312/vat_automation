<template>
    <b-card no-body>
        <b-tabs pills card vertical>
            <b-tab title='Overview' active>
                <p>self name: {{ self.name }}</p>
                <overview :self="self" />
            </b-tab>
            <b-tab title='Add Clients'>
                <add-client />
            </b-tab>
            <b-tab title='Add Data'>
                <add-seller-firm-data />
            </b-tab>
        </b-tabs>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        layout: 'tax',
        middleware: "auth-tax",
        computed: {
            ...mapState({
                self: state => state.auth.user,
            })
        },


        // async fetch({ $axios, store }) {
        //     let [response_self, response_employer_clients] = await Promise.all([
        //         $axios.$get('/user/tax_auditor/self'),
        //         $axios.$get('/business/seller_firm/as_client')
        //     ]);

        //     const self = response_self.data
        //     const employer_clients = response_employer_clients.data

        //     store.commit('SET_SELF', self)
        //     store.commit('SET_EMPLOYER_CLIENTS', employer_clients)
        // }
    };
</script>

<style></style>
