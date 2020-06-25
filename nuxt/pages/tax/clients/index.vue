<template>
    <b-card no-body>
        <b-tabs pills card vertical>
            <b-tab title='Overview' active>
                <Overview />
            </b-tab>
            <b-tab title='Add Clients'>
                <AddClient />
            </b-tab>
            <b-tab title='Add Data'>
                <AddSellerFirmData />
            </b-tab>
        </b-tabs>
    </b-card>
</template>

<script>
    // import AddClient from '@/components/TaxAuditor/Clients/AddClient';
    // import Overview from '@/components/TaxAuditor/Clients/Overview';

    export default {
        layout: 'tax',
        // components: {
        //     AddClient,
        //     Overview
        // },
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
