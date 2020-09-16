<template>
    <b-card no-body>
        <b-tabs pills card vertical>
            <b-tab title='Overview' @click="refresh" active>
                <clients-dashboard />
                <view-clients class="mt-5"/>
            </b-tab>
            <b-tab title='Add Clients' lazy>
                <lazy-container-add-client/>
            </b-tab>
        </b-tabs>
    </b-card>
</template>

<script>
    import { mapState } from "vuex";

    export default {
        layout: 'tax',

        computed: {
            ...mapState({
                accounting_firm: state => state.accounting_firm.accounting_firm
            }),

            countClients() {
                return this.$store.getters['accounting_firm/countClients']
            },
        },

        methods: {
            async refresh() {
                const { store } = this.$nuxt.context
                await store.dispatch("accounting_firm/get_by_public_id", this.accounting_firm.public_id)
            }
        },
    };
</script>

<style></style>
