<template>
    <b-card no-body>
        <b-tabs pills card vertical>
            <b-tab title='Overview' @click="refresh" active>
                <clients-dashboard />
                <view-clients class="mt-5"/>
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
                accounting_firm: state => state.accounting_firm.accounting_firm
            })
        },


        methods: {
            setLoadingToFalse() {
                this.loading = false
            },
            async refresh() {
                const { store } = this.$nuxt.context
                await store.dispatch("accounting_firm/get_by_public_id", this.accounting_firm.public_id)
            }
        }




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
